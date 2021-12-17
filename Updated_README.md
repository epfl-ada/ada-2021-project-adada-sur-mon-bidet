# Polarization around climate change: 
## Is it growing as fast as the polar circle is shrinking? 

## Abstract:
As the effects of climate change become increasingly visible in our daily life, it is time for humanity to come together for a joint effort to come back to an equilibrium with nature. A joint effort requires collaboration and agreement on what climate change is and what we should do. In this data story, we will study the polarization of opinions around climate change that tend to make this collaboration difficult to accomplish and examine its dynamics. This will be done through the lens of Quotebank, an open corpus of 178 million quotations attributed to the speakers who uttered them, extracted from 162 million English news articles published between 2008 and 2020.


## Data Story

Our data story can be found here: INSERT URL

## Research questions:

- Who talks about climate, who is most often quoted?
- How does the narrative about climate change evolve from 2015 to 2020? Is it increasingly polarized? 
- If it is polarized, what influences it? (political acquaintance, profession, ...) 
- Does the narrative concentrate on polemic topics?

## Additional datasets:
Wikipedia will be used to fetch more information about each quoted person.

## Methods:

### Preprocessing

We filtered the original Quotebank 2015-2020 JSON files, keeping only quotations with known speakers (certainty > 0.9) and containing a word related to climate change. To distinguish "words relating to climate change", we constructed a hand-curated dictionary. This dictionary contains 62 words that cover all the topics specific to climate change. We will refer to these topics throughout our data story. Going further, we made sure to reduce the false positive rate around certain topics like "energy" or "atmosphere" which tend to talk more about football games than climate.


In the rest of our analysis, we assume that the quotes that we are working on in the following sections should all have the theme of climate change.

### Examining the people driving the climate change narrative

To understand and exploit text data to its fullest, it is important to understand the context and origin of the data. In the case of Quotebank, this boils down to understanding who is quoted. 

To achieve this goal, we use Wikipedia data to associate features to our speakers such as age, gender and political party.

Using these features, we can come up with a global view of the speakers in our dataset.

### How to measure and extract polarization ?:

We define polarization as *: a state in which the opinions, beliefs, or interests of a group or society no longer range along a continuum but become concentrated at opposing extremes.*

In our case, we measure the polarization of these different quotes by a combination of sentiment analysis(polarity of sentiment) and the "separation" of quotes in their semantics/meaning. "I hate" or "I love" are two very opposite sentiments, but there's also a clear difference in their meaning. 

 We use two methods: sentiment analysis and word embedding

Sentiment analysis is a technique that allows us to extract, identify and quantify affect states in text. Sentiment analysis will let us assign a "sentiment" polarity score to a quote. This score spans the interval [-1,1] with -1 being extremely negative and 1 being extremely positive.

 Word embedding aims to quantify and categorize semantic similarities between linguistic items. To put it simply, word embedding maps a word to a "semantic space" i.e. N-dimensional space where words with very different meanings should have a large distance between them. Therefore, in theory, two quotes at the different ends of the spectrum should have a large distance between them and this would let us compute a "polarity distance" between quotes. 


### How to study and visualize polarization ?:

Using our polarity score, we can now plot the polarity score of our corpus. We first examine global trends with different time granularity (yearly, monthly, daily). Afterward, we examine the narrative of precise climate change topics. More precisely, we define, using a heuristic, how controversial a topic is. Using this measure, we examine specifically polemic and non-polemic topics.

Furthermore, we use word embedding with the help of PCA to project the quotes in 3D space and examine the semantic space separation. This allows us to assess the semantic difference between speeches that are polarized positively and negatively. We can try to assess the evolution, throughout time, of this semantic difference. The bigger it is, the more the speeches are different in their vocabulary and argumentation. Thus, the polarized group tends to be more and more opposed.

Finally, we combine the speakers' features and polarity score to get an overview of how polarity evolves depending on political party to wrap up.


## Organization within the team:

- *Paul Juillard*: Preprocessing and clustering
- *Antoine Magron*: Word embedding and topic analysis
- *Lucas Trognon*: Analysis of the people driving the climate change narrative
- *Harold Benoit*: Evolution and visualization of polarization  




