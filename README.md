# Polarization around climate change: 
## Is it growing as fast as the polar circle is shrinking ? 

## Abstract:
As the effects of climate change become increasingly visible in our daily life, it is time for humanity to come together for a joint effort to come back to an equilibrium with nature. A joint effort requires collaboration and agreement on what climate change is and what we should do. In this data story, we will study the polarization of opinions around climate change that tend to make this collaboration diffcult to accomplish, and examine its dynamics. This will be done through the lense of Quotebank, an open corpus of 178 million quotations
attributed to the speakers who uttered them, extracted from 162 million English news articles published between 2008 and 2020.



## Research questions:

- Who talks about climate, who is most often quoted?
- How does the narrative about climate change evolve from 2015 to 2020 ? Is it increasingly polarized ? 
- If it is polarized, what influences it ? (political acquaintance, profession, ...) 
- Bonus:
    - Does the narrative concentrate around buzzwords ?
    - Is the narrative influenced by major events (does it polarize more when certain events occur)

## Additional datasets:
Nothing yet

## Methods:

### Preprocessing

We filtered the original Quotebank 2015-2020 json files, keeping only quotations with known speakers (certainty > 0.9) and contains a word related to climate change. To distinguish "words relating to climate change", we constructed a 'base' dictionnary from various online sources, and a 'wide' dictionnary of more questionnable pertinence, which extends the basis with nltk's wordnet. Also, urls are stripped to domain names as we do not intend to access the full articles. Results of this preliminary filtering are in the 'output' directory.

These new jsons are further preprocessed into yearly chunks of 500 000 quotations and saved in pickle format to reduced loading times. These are also found in the 'output' directory as 'df_year_chunkidx'.

We assume that the quotes that we are working in the following sections should all have the theme of climate change. 

### How to measure and extract polarization ?:

First, let us define polarization.

*Polarization : a state in which the opinions, beliefs, or interests of a group or society no longer range along a continuum but become concentrated at opposing extremes.*

In our case, we expect polarization to occur on the two ends of the "do I believe climate change is real and something should be done about it?" where either people totally reject the idea of climate change or they can be very alarmistic. 

In our case, we will try to measure polarization of these different quotes by a combination of sentiment analysis(polarity of sentiment) and the "separation" of quotes in their semantics/meaning. "I hate" or "I love" are two very opposite sentiments but there's also a clear difference in their meaning. Below, we explain the methods that will let us mathematically extract these qualities.


 We will use two methods : sentiment analysis and word embeddings

Sentiment analysis is a technique that allows us to extract, identify and quantify affective states in text. The most basic task of sentiment analysis is classifying and quantifying the polarity of a given text in 3 classes {positive, neutral, negative}. Sentiment analysis will let us assign a "sentiment" polarity score to a quote. After reviewing the literature on sentiment analysis, we decided not to train our own classifier but to use an already exisiting tool. We are using VADER[^fn1] (Valence Aware Dictionary and sEntiment Reasoner), a lexicon and rule-based sentiment analysis tool. It is specifically attuned to sentiments expressed in social media but it has been shown to generalize very well. Furthermore, it is able to account for differences in the sentiment intensity of words using the sentiment valence (continous feature ranging from -1 to 1). For example, the valence for betray is -0.83, bland is -0.2475, dream is 0.4325, and delight is 0.815. This will let us capture more accurately the true extremes.

The ideal goal would be to assign a single or multiple metrics to a quote that quantifies accurately its polarization we defined above.

 Word embeddings aim to quantify and categorize semantic similarities between linguistic items based on their distributional properties in large samples of language data. The underlying idea that "a word is characterized by the company it keeps". To put it simply, word embeddings map a word to a "semantic space" i.e. N-dimensional space where words with very different meanings should have a large distance between them. Therefore, in theory, two quotes at the different ends of the spectrum should have a large distance between them and this would let us compute a "polarity distance" between quotes. Additionally, one might use clustering to group similar quotes and hope to get that quotes in the same cluster share the same opinion.

 Although, one needs to be cautious before using word embeddings.

COMMENT OUT (Word embeddings might not give us enough separation between positive and negative quotes since most of the words in a quote will be "neutral" and in the theme of climate change (e.g. "climate","warming","environment"). Thus, to only retain important information about the tone of the quote, one would further need to filter out climate-related words such that the semantic space is better separated.)




### How to visualize polarization ?:

One can use word embeddings with the help of PCA to project the quotes in 3D space.One would hope that one of the principal components is polarity but that might not be the case. Our polarity score, previously computed, should let us check if it is the case.

One can also use our polarity score and plot it under multiple discriminants (time, specific words, speaker profession).

### Extracting evolution trends and major events:

Time series analysis comes to the rescue. After our work of quantifying polarization, one can simply use time series analysis to extract the seasonality + trend + noise components of a time series to answer a few questions.

Extracting the trend would let us answer the question of whether polarization increases over time.

Seasonality would let us observe if there's any recurring event (climate conference, ...) affecting polarization.


## Proposed timeline:

- Preprocessing 
- Word embedding pipeline
- Sentiment analysis pipeline and polarization score
- Visualisation
- Time series analysis
- Data story

## Organization within the team:

- *Paul Juillard*: bg frais, preprocessing expert
- *Antoine Magron*: slim seductor, word embedding magician
- *Lucas Trognon*: curly stud, wikipedia dump adept
- *Harold Benoit*: sentiment analysis boi


## Questions for TAs:


[^fn1]: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
