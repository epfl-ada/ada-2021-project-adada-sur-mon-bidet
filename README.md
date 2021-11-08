# Title : 

## Abstract:


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

### How to measure and extract polarization ?:

First, let us define polarization.

__Polarization : a state in which the opinions, beliefs, or interests of a group or society no longer range along a continuum but become concentrated at opposing extremes.__

In our case, we expect polarization to occur on the two ends of the "do I believe climate change is real and something should be done about it?" where either people totally reject the idea of climate change or they can be very alarmistic. 

In our case, we will try to measure polarization of these different quotes by a combination of sentiment analysis(negative and positive sentiments are on opposite side of the spectrum) and the "separation" of quotes in their semantics/meaning. "I hate" or "I love" are two very opposite sentiments but there's also a clear difference in their meaning. Below, we explain the methods that will let us mathematically extract these qualities.


 We will use two methods : sentiment analysis and word embeddings



Sentiment analysis is the 

 Word embeddings aim to quantify and categorize semantic similarities between linguistic items based on their distributional properties in large samples of language data. The underlying idea that "a word is characterized by the company it keeps". To put it simply, word embeddings map a word to a "semantic space" i.e. N-dimensional space where words with very different meanings should have a large distance between them. 

 After some quali preprocessing where we only retain quotes whose theme is around cliamte, one needs to be cautious before applying the different methods.

Word embeddings might not give us enough separation between positive and negative quotes since most of the words in a quote will be "neutral" and in the theme of climate change (e.g. "climate","warming","environment"). Thus, to only retain important information about the tone of the quote, one would further need to filter out climate-related words such that word embeddings can separate much better.


The ideal goal would be to assign a single or multiple metrics to a quote that quantifies accurately its polarization

### How to visualize polarization ?:

One can use word embeddings with the help of PCA to project the quotes in 3D space.

One can also use our polarity score and plot it under multiple discriminants.

### Extracting evolution trends and major events:

Time series analysis comes to the rescue. After our work of quantifying polarization, one can simply use time series analysis to extract the seasonality + trend + noise components to answer a few questions.

Extracting the trend would let us answer the question of whether polarization increases over time.

Seasonality would let us observe if there's any recurring event (climate conference, ...) affecting polarization.


## Proposed timeline:

## Organization within the team:

## Questions for TAs:


