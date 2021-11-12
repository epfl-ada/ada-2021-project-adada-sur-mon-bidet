# Polarization around climate change: 
## Is it growing as fast as the polar circle is shrinking? 

## Abstract:
As the effects of climate change become increasingly visible in our daily life, it is time for humanity to come together for a joint effort to come back to an equilibrium with nature. A joint effort requires collaboration and agreement on what climate change is and what we should do. In this data story, we will study the polarization of opinions around climate change that tend to make this collaboration difficult to accomplish and examine its dynamics. This will be done through the lens of Quotebank, an open corpus of 178 million quotations
attributed to the speakers who uttered them, extracted from 162 million English news articles published between 2008 and 2020.


## Research questions:

- Who talks about climate, who is most often quoted?
- How does the narrative about climate change evolve from 2015 to 2020? Is it increasingly polarized? 
- If it is polarized, what influences it? (political acquaintance, profession, ...) 
- Bonus:
    - Does the narrative concentrate on buzzwords?
    - Is the narrative influenced by major events?
    - What are the steps one should follow to bring a subject to the world's attention (at least the US)

## Additional datasets:
Wikipedia will be used to fetch more information about each quoted person.

## Methods:

### Preprocessing

We filtered the original Quotebank 2015-2020 json files, keeping only quotations with known speakers (certainty > 0.9) and contains a word related to climate change. To distinguish "words relating to climate change", we constructed a 'base' dictionnary from various online sources, and a 'wide' dictionnary of more questionnable pertinence, which extends the basis with nltk's wordnet. Also, urls are stripped to domain names as we do not intend to access the full articles. Results of this preliminary filtering are in the 'output' directory.

These new jsons are further preprocessed into yearly pickles to reduce loading times.

We assume that the quotes that we are working on in the following sections should all have the theme of climate change.

### How to measure and extract polarization ?:

First, let us define polarization.

*Polarization: a state in which the opinions, beliefs, or interests of a group or society no longer range along a continuum but become concentrated at opposing extremes.*

In our case, we expect polarization to occur on the two ends of the "do I believe climate change is real and something should be done about it?" where either people totally reject the idea of climate change or they can be very alarmist. 

In our case, we will try to measure the polarization of these different quotes by a combination of sentiment analysis(polarity of sentiment) and the "separation" of quotes in their semantics/meaning. "I hate" or "I love" are two very opposite sentiments but there's also a clear difference in their meaning. Below, we explain the methods that will let us mathematically extract these qualities.

 We will use two methods: sentiment analysis and word embedding

Sentiment analysis is a technique that allows us to extract, identify and quantify affect states in text. The most basic task of sentiment analysis is classifying and quantifying the polarity of a given text in 3 classes {positive, neutral, negative}. Sentiment analysis will let us assign a "sentiment" polarity score to a quote.

 Word embedding aims to quantify and categorize semantic similarities between linguistic items based on their distributional properties in large samples of language data. To put it simply, word embedding maps a word to a "semantic space" i.e. N-dimensional space where words with very different meanings should have a large distance between them. Therefore, in theory, two quotes at the different ends of the spectrum should have a large distance between them and this would let us compute a "polarity distance" between quotes. Additionally, one might use clustering to group similar quotes and hope to get that quotes in the same cluster to share the same opinion.

 

Nevertheless, word embedding might not give us enough separation between positive and negative quotes since most of the words in a quote will be "neutral" and in the theme of climate change (e.g. "climate", "warming", "environment"). To only retain important information about the tone of the quote, one would further need to filter out climate-related words such that the semantic space is better separated. 

The ideal goal would be to assign a single or multiple metrics to a quote that quantifies accurately the polarization we defined above as done in this [paper](https://ieeexplore.ieee.org/document/8181508).

### How to visualize polarization ?:

One can use word embedding with the help of PCA to project the quotes in 3D space. One would hope that one of the principal components is polarity but that might not be the case. Our polarity score, previously computed, should let us check if it is the case.

One can also use our polarity score and plot it under multiple discriminators (time, specific words, speaker profession).

### Extracting evolution trends and major events:

Time series analysis comes to the rescue. After our work of quantifying polarization, one can simply use time series analysis to extract the seasonality + trend + noise components of a time series to answer a few questions.

Extracting the trend would let us answer the question of whether polarization increases over time.

Seasonality would let us observe if there's any recurring event (climate conference, ...) affecting polarization.

### Confronting our observations with the demographic

Now that we have the evolution of the polarization over time, we can try to spot some correlation between the polarization clusters and the profile of the speakers. Namely their gender, age, and political affiliation (we might expand to more features in the future). 

To do so, we are fetching the Wikipedia page of each speaker and are running some rough (but surprisingly relatively accurate) heuristics to guess all of those features. 


## Proposed timeline:

- Preprocessing 
- Word embedding pipeline
- Sentiment analysis pipeline and polarization score
- Visualization
- Time series analysis
- Data story

## Organization within the team:

- *Paul Juillard*: preprocessing expert
- *Antoine Magron*: word embedding magician
- *Lucas Trognon*: Wikipedia dump adept
- *Harold Benoit*: sentiment analysis guru


## Questions for TAs:


