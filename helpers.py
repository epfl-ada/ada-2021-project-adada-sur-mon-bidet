import bz2
import json
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import scipy.stats as stats
import scipy
from astropy.stats import bootstrap
from functools import reduce
from gensim.models import Word2Vec, KeyedVectors
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
import matplotlib.pyplot as plt


nltk.download('stopwords')

stopwords = stopwords.words()

__path_to_file = 'data/quotes-2020.json.bz2' 


__SAMPLE_SIZE = 10


__MODEL_FILE = "vectors.txt"


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


def get_samples(filename=__path_to_file, num_samples=__SAMPLE_SIZE, random=False):
    dict = {}
    index = range(num_samples)
    if(random):
        index = np.random.randint(0, high=50_000, size=num_samples)

    
    with bz2.open(filename, 'rb') as s_file:
        for i, instance in zip(range(max(index)), s_file):
            if(i in index):
                dict[i] = eval(json.dumps(json.loads(instance)))
    return pd.DataFrame.from_dict(dict, orient="index")


def __compose (*functions):
    def inner(arg):
        for f in functions:
            arg = f(arg)
        return arg
    return inner

### TEXTUAL PREPROCESSING PART

def to_lower(prep_text):
    return prep_text.lower()

def to_text(prep_text):
    return re.sub('[^a-zA-Z]+', ' ', prep_text)

def get_tokens(prep_text):
    return nltk.tokenize.word_tokenize(prep_text)


def remove_stop_words(tokens):
    return  [word for word in tokens if not word in stopwords]

def adds_bigram(tokens):
    return list(tokens) + list(map(lambda tok : " ".join(tok), nltk.ngrams(tokens, 2)))


preprocess = __compose(to_lower, to_text, get_tokens, remove_stop_words, adds_bigram)

def preprocess_quote(quote):
    return preprocess(quote)


def save_model(model_filename=__MODEL_FILE):
    model = KeyedVectors.load_word2vec_format(model_filename, binary=False)
    model.save("W2V.model")

def get_model(model_filename="W2V.model"):
    return KeyedVectors.load(model_filename)


def aggregate(model, prep_quote):
    vecs = None
    
    for token in prep_quote:
        vec = None 
        
        try :
            vec = model.get_vector(token)
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
    


def get_w2c_matrix(model, data, column):
    quotes = data[column].apply(lambda quote : aggregate(model, quote))

    vecs_quote = []
    for quote in quotes :
        vecs_quote.append(quote)

    return np.vstack(vecs_quote)
    


def show_w2v_words(X, kmeans=None, ):
    fig = plt.figure(1, figsize=(10, 10))
    plt.clf()
    ax = Axes3D(fig, rect=[1, 1, 1, 1], elev=48, azim=134)

    plt.cla()
    pca = decomposition.PCA(n_components=3)
    idx = np.random.randint(len(X), size=round(len(X)/5))
    pca.fit(X[idx, :])
    X_proj = pca.transform(X[idx, :])
    

    if(kmeans is not None):
        center_proj = pca.transform(kmeans.cluster_centers_)
        for i, center in  enumerate(center_proj):
            ax.text3D(center[0], center[1], center[2], str(i), horizontalalignment='center',bbox=dict(alpha=.5, edgecolor='w', facecolor='r'))
    # Reorder the labels to have colors matching the cluster results1
    ax.scatter(X_proj[:, 0], X_proj[:, 1], X_proj[:, 2], cmap=plt.cm.nipy_spectral,
            edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

    plt.show()