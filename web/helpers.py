
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
from astropy.stats import bootstrap
from functools import reduce
from gensim.models import KeyedVectors
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
import matplotlib.pyplot as plt
import os
from PIL import Image
from matplotlib import cm
from time import time
import threading
from multiprocessing import Process, Array



nltk.download('stopwords')
nltk.download("punkt")
    
stopwords = stopwords.words()

__path_to_file = 'data/quotes-2020.json.bz2' 


__SAMPLE_SIZE = 10


__MODEL_FILE = "vectors.txt"

#par_context = Context()
par_context = None




def CIs(data, columns, funcs, interval=(2.5, 97.5)):
    """
    computes 95% confidence interval for any column and inputed statistics
    
    input :
        - data : the dataframe on which you want to work
        - columns : list of the names of the columns of the dataframe you want to study
        - funcs : list of the statistics you compute as list [callable function]
    
    returns :
        - a dataframe containing for each column, the low value and the high value (in two difference lines)
        composing the confidence interval
    """
    low, high = interval
    cols = {}
    named_func = [[func.__name__, func] for func in funcs]
    for feature in columns :
        col = np.array([])
        studied_vals = data[feature].dropna(how='any').values
        for func_name, func in named_func:
            boots = bootstrap(studied_vals, bootfunc=func)
            ci = [np.nanpercentile(boots, low),np.nanpercentile(boots, high)]
            col = np.append(np.append(np.append(col, ci[0]), func(studied_vals)), ci[1])
        cols[feature] = col
    index = reduce(lambda x, y : x + y, [[f"{func_name}_low", f"{func_name}_computed", f"{func_name}_high"] for func_name, func in named_func])
    CI_df = pd.DataFrame.from_dict(cols) 
    CI_df.index = index
    return CI_df



def __compose (*functions):
    """
    create a compositions of multiple functions
    """
    def inner(arg):
        for f in functions:
            arg = f(arg)
        return arg
    return inner

### TEXTUAL PREPROCESSING PART

def to_lower(prep_text):
    """
    put every quotation in lowercase
    """
    return prep_text.lower()

def to_text(prep_text):
    """
    removes every character that isn't a letter
    """
    return re.sub('[^a-zA-Z]+', ' ', prep_text)

def get_tokens(prep_text):
    """
    tokenize the text (words)
    """
    return nltk.tokenize.word_tokenize(prep_text)


def remove_stop_words(tokens):
    """
    removes evert stopwords
    """
    return  [word for word in tokens if not word in stopwords]

def adds_bigram(tokens):
    """
    Adds the bigrams in the prep_quotes
    """
    if(len(tokens) == 0):
        return tokens
    return list(tokens) + list(map(lambda tok : " ".join(tok), nltk.ngrams(tokens, 2)))


preprocess = __compose(to_lower, to_text, get_tokens, remove_stop_words, adds_bigram)

def preprocess_quote(quote):
    """
    preprocesses a quotation
    """
    return preprocess(quote)

def __unit_preprocess(quotes, indx):
    quotes[indx] = preprocess_quote(quotes[indx])



def par_preprocess_data(data, quote_col="quotation"):
    """
    parallel run of the preprocessing : useless since no improvement
    """
    quotes = data[quote_col].values

    threads = []
    for i in range(len(quotes)):
        ## we got through all the entries of the array
        
        unit_thread = threading.Thread(target=__unit_preprocess, args=(quotes, i))
        threads.append(unit_thread)
        unit_thread.start()
    
    
    [ut.join() for ut in threads]

    return quotes
    





################## WORD 2 VEC
def save_model(model_filename=__MODEL_FILE):
    model = KeyedVectors.load_word2vec_format(model_filename, binary=False)
    model.save("W2V.model")

def get_model(model_filename="W2V.model"):
    """
    load the word 2 vec model
    """
    return KeyedVectors.load(model_filename)


def aggregate(model, prep_quote):
    """
    takes all the vector in a setence and aggregate it in only one vector (by taking the average)
    """
    vecs = None
    
    for token in prep_quote:
        vec = None 
        
        try :
            #vec = model.get_vector(token)
            vec = model[token]
        except :
            pass
        if(len(prep_quote) == 1):
            return vec
        if(vecs is None) :
            vecs = vec
        else :
            if(vec is not None):
                vecs = np.vstack([vecs, model.get_vector(token) if " " not in token else ((model.get_vector(token[0]) + model.get_vector(token[1]))/2) ])
    if vecs is None:
        return np.zeros(300).astype(np.float32)
    
    if(vecs.shape == (300,)):
        return vecs
    return np.mean(vecs, axis=0)


def get_default_vec(model, all_words):
    return aggregate(model, all_words)
    


def get_w2c_matrix(model, data, column, labels):
    """
    takes, for all the sentence in column in data and returns the vectorize version
    """
    ### returns the vectors and the labels
    quotes = data[column].apply(lambda quote : aggregate(model, quote))
    
    vecs_quote = []
    indices = []
    for idx, quote in enumerate(quotes) :
        if(quote is not None and quote.shape == (300,)):
            vecs_quote.append(quote)
            indices.append(idx)
            
    
    data[labels][data[labels] >= 0.282] = 1
    data[labels][data[labels] < 0.282] = -1
    return np.vstack(vecs_quote), (data[labels].values)[indices]
    


######################## VECTOR SPACE STUDY
def center_of_mass(vec_space):
    """
    return the mean of a vectors
    """
    return np.mean(vec_space, axis=0)


def euclidean_dist(center1, center2):
    """
    computes the distance between two points (euclidean distance)
    """
    return np.sum((center1 - center2)**2)


def cosine_sim(center1, center2):
    """
    computes the cosine similarity between two points
    """
    
    return np.nansum(center1 * center2) / (np.linalg.norm(center1) * np.linalg.norm(center2))


def __dist(model, single_point, X):
    """
    computes the cosine similarity between a single point and every point in X
    """
    
    #return (((X @single_point) / np.sum(X ** 2, axis=1))) / (np.linalg.norm(single_point))
    return np.sqrt(np.sum((X - single_point)**2, axis=1))
    #return model.distances(single_point, X)


def normalized_cut(model, set1, set2):
    """
    compute the normalized cut between two sets if word to vec vectors
    """
    ### MemoryError: Unable to allocate 17.2 GiB for an array with shape (7683983, 2, 300) and data type float32
    # pairs = np.array(list(itertools.product(set1, set2)))
    # d_ = lambda pair : d(pair[0], pair[1])
    # return d_(pairs)

    d12 = 0
    d1 = 0
    for x in set1:
        d1 += np.nansum(__dist(model, x, set1))
        d12 += np.nansum(__dist(model, x, set2))


    d2 = 0
    for x in set2:
        d2 += np.nansum(__dist(model, x, set2))
    

    return (d12 / (d12 + d1)) + (d12 / (d12 + d2))








################# GRAPHS :
def show_w2v_words(X, kmeans=None, outfilename="W2V.png", colors=None, dimensions=3, yield_ax=False, yield_pca=False, show=True, download=True):
    """
    Displays the word2vec vectors projected in either 2 or 3 dimensions
    (in PCA). It downloads the image in outfilename and each points takes 
    the color given in colors array
    """
    fig, ax = plt.subplots(1, figsize=(10, 10))
    if(dimensions == 3):
        #plt.clf()
        #fig.add_subplot(111, projection="3d")
        ax = Axes3D(fig, rect=[1, 1, 1, 1], elev=48, azim=134)
    
        plt.cla()
        pca = decomposition.PCA(n_components=3)
        
        pca.fit(X)
        X_proj = pca.transform(X)
        if(colors is not None):
            colors_proj = colors
        
        
    
        if(kmeans is not None):
            center_proj = pca.transform(kmeans.cluster_centers_)
            for i, center in  enumerate(center_proj):
                pass
                #plt.text3D(center[0], center[1], center[2], str(i), horizontalalignment='center',bbox=dict(alpha=.5, edgecolor='w', facecolor='r'))
        # Reorder the labels to have colors matching the cluster results1
        if(colors is None):
            ax.scatter(X_proj[:, 0], X_proj[:, 1], X_proj[:, 2], cmap=plt.cm.nipy_spectral,
                edgecolor='k')
        else :
            ax.scatter(X_proj[:, 0],X_proj[:, 1], X_proj[:, 2], color=colors_proj,
                edgecolor='k')
    
        fig.tight_layout()
    elif (dimensions == 2):
        pca = decomposition.PCA(n_components=2)
        
        pca.fit(X)
        X_proj = pca.transform(X)
        
        if(colors is not None):
            colors_proj = colors
        
            
        if(colors is None):
            plt.scatter(X_proj[:, 0], X_proj[:, 1], cmap=plt.cm.nipy_spectral,
                edgecolor='k')
        else :
            plt.scatter(X_proj[:, 0],X_proj[:, 1], color=colors_proj,
                edgecolor='k')
        
    
    if(dimensions == 2 and download):    
        fig.savefig(outfilename, dpi=150, format="png")
        print(">>> saving at ", outfilename)
    if(show):
        plt.show()
    
    if(yield_ax and yield_pca):
        return ax, pca
    if(yield_ax):
        return ax
    if(yield_pca):
        return pca


def generate_gif(outfile_name, infile_names):
    """
    generates a GIF using all the files given in infile_names. 
    It writes the GIF in outfile_name
    """
    outgif = Image.new('RGB', (1500,1500))
    ims = [Image.open(name) for name in infile_names]
    try : 
        outgif.save(outfile_name, save_all=True, append_images=ims, duration=len(infile_names)*10)
    finally :
        [im.close() for im in ims]
    
    



def get_cmap_from_labels(labels):
    """
    outputs a colormap using the chosen labels of each datapoints
    """
    u_colors = np.unique(labels)
    #u_colors = [0, 1]
    
    colors = cm.get_cmap('magma', len(u_colors))

    cmap = {}
    for i, color in enumerate(u_colors):
        cmap[color] = colors.colors[i]
    
    
    cmap={-1 : 'red', 1 : 'blue'}
    cols = []
    for label in labels:
        cols.append(cmap[label])

    return np.hstack(cols)


def bootstrap_f(model, cpos, cneg, f):
    stats = []
    for i in range(100):
        cpos_here = np.random.choice(cpos, replace=True, size=10000)
        cpos_here = np.random.choice(cpos, replace=True, size=10000)
        stats.append(f(model, cpos_here, cneg_here))
    
    stats.sort()
    return stats[5], stats[-5]
        
    
    


def process(data, model,sentiment, par=False):
    """
    processing pipeline that can do the preprocessing parallely or not (with boolean par).
    for each month, the processing is done **sequentially** and can thus be quite slow.
    """
    start = time()


    if(not par):
        df["prep_quote"] = df.quotation.apply(preprocess_quote) ## preprocess quotes
    else :
        df["prep_quote"] = par_preprocess_data(df) ## preprocess quotes
    

    ## adds random sentiment
    

    ## get all the datapoints (one per quote) in W2V vector space
    vec_spaces, labels = zip(*df.groupby("month").apply(lambda x : get_w2c_matrix(model, x, "prep_quote", sentiment)).values)

    [show_w2v_words(vec_space, outfilename=f'W2V{idx}.png', colors=get_cmap_from_labels(labels[idx])) for idx, vec_space in enumerate(vec_spaces)]

    return time() - start


def par_process(totdata, model, sentiment="compound", benchmark=False, display_dims=2):
    """
    equivalent of process (execution pipeline) but goes through all the month parallely. 
    The overall speedup made by the parallelization is not that impressive.
    """
    def unit_process(data, date, metrics, benchmark, idx):
        ## extract the color vec spaces
        
        #data["prep_quote"] = data["quotation"].apply(preprocess_quote)
        vec_space, labels = get_w2c_matrix(model, data, "prep_quote", sentiment)
        show_w2v_words(vec_space, outfilename=f"medias/W2V{idx}.png", colors=get_cmap_from_labels(labels), dimensions=display_dims)
        
        
        cneg = vec_space[labels < 0]
        cpos = vec_space[labels >= 0]
        #metrics[idx] = normalized_cut(model, cpos, cneg)
        metrics[0][idx] = cosine_sim(center_of_mass(cpos), center_of_mass(cneg))
        f = lambda model, cpos, cneg: cosine_sim(center_of_mass(cpos), center_of_mass(cneg))
        lbound, ubound = bootstrap_f(model, cpos, cneg, f)
        metrics[1][idx] = lbound
        metrics[2][idx] = ubound
    
    start = time()    
    
    
    totdata["dayless_date_verbose"] = pd.to_datetime(totdata.date).dt.strftime('%b-%Y')
    totdata["dayless_date"] = pd.to_datetime(totdata.date).apply(lambda t : t.replace(day=1, hour=0, minute=0, second=0))
    
    
    
    grouped = totdata.sort_values("dayless_date").groupby("dayless_date")
    
    
    
    print("computed month discriminant")
    subprocesses = []
    
    ## concurrent Array for every process to write its result
    metrics = Array("d", len(grouped))
    l_bounds = Array("d", len(grouped))
    u_bounds = Array("d", len(grouped))
    
    for idx, df in enumerate(grouped):
        ## go through every subdataframe
         unit = Process(target=unit_process, args=(df[1], df[0], (metrics, l_bounds, u_bounds), benchmark, idx))
         
         unit.start()
         print(str(idx), ") launch thread ", df[0])
         subprocesses.append(unit)
        
    print("wait for everything to join")
    [ut.join() for ut in subprocesses]
    
    print("done")
    if(benchmark):
        return time() - start
    
    f_indices = range(len(list(grouped)))
    if(display_dims == 2):
        filenames = [f"medias/W2V{i}.png" for i in f_indices]
        print("GENERATING THE GIF")
        generate_gif("finalGIF.GIF", filenames)
    
    return metrics, l_bounds, u_bounds
    


def show_quote_in_set(vec_space, dimensions, colors, quote_point, show=True):
    fig, ax = plt.subplots(1, figsize=(10, 10))
    
    ## projection :
    pca = decomposition.PCA(n_components=2)
    pca.fit(vec_space)
    X_proj = pca.transform(vec_space)
    quote_point = pca.transform(quote_point)[0]
    
    ## plot
    plt.scatter(X_proj[:, 0],X_proj[:, 1], color=colors, edgecolor='k')
    
    ax.plot(quote_point[0], quote_point[1], markerfacecolor="green", marker="o", markersize="20")
    ax.annotate(str("you are here!"), (quote_point[0], quote_point[1]), fontsize=20, color="yellow")
    fig.savefig("web/static/W2V_quote.png", dpi=300)

    
        
    
    
        
    
    
    
    


    
    

version = 55