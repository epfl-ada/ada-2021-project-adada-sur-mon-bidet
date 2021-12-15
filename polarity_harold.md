## How do we speak about climate ? The fine details of its narrative in the news



### What is polarization ?


Let us define polarization.

*Polarization: a state in which the opinions, beliefs, or interests of a group or society no longer range along a continuum but become concentrated at opposing extremes.*

In our case, we will try to measure the polarization of these different quotes by sentiment analysis i.e. polarity of sentiment.


### Evaluating polarization:

Given a sentence, we use VADER(Valence Aware Dictionary and sEntiment Reasoner) to compute the polarity score.

Valence, or hedonic tone, is the affective quality referring to the intrinsic attractiveness/"good"-ness (positive valence) or averseness/"bad"-ness (negative valence) of an object, in our case, text. The term also characterizes and categorizes specific emotions. For example, emotions popularly referred to as "negative", such as anger and fear, have negative valence. Joy has positive valence.

 Thus, our polarity score score is computed by summing the valence scores of each word in the quotation, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive).


### Evolution of polarization

Given this polarity score assigned to each quotation, we can now study its behaviour under multiple point of views (time, age, gender, political party) and look at if certain topics arise as more dividing than others.


#### Polarity score distribution throughout all quotations

Let us first look at the distribution of polarity score throughout 2015 to 2020.

![Distribution of polarity scores]( notebooks/harold/figs/total_polarity_distribution.png "Distribution of polarity scores")

As we can see (warning, log scale !), a majority of the quotations are considered neutral (score of 0.0).

The mean polarity score in our corpus is 0.27 with a standard deviation of 0.49. 

#### Polarity score for each year

Let us look at the distribution of each year to see if there's any year that stands out.

![Distribution of polarity scores for each year]( notebooks/harold/figs/boxplot_year.png "Distribution of polarity scores for each year")

As we can see, polarity seems to be very constant throughout the years. Similarly, we looked throughout the months and didn't find anything significant.

Maybe, all we need is finer granularity ! Let's look at the daily average polarity score throughout the years.


![Average polarity score throughout the years]( notebooks/harold/figs/average_daily_polarity.png "Average polarity score throughout the years")


Looking at the 2016 period, we might think that we have caught onto a particularly polarized period in the news! Who knows what very polarizing event happened during 2016 in the USA ? 

But looking closely, it's a matter of having much less data during 2016 which makes the mean very sensitive to outliers. Tough luck....

Therefore, as we can see, the average daily sentimental polarity of the quotation on climate change throughout the years is quite stable at around 0.27!


### Polemic topics 

After seeing that there was no noticeable evolution of the polarization of the narrative around climate change in a global scale, we decided to dig a little further and examine the narrative around specific topics.

Polemic topics and polarization go hand in hand, therefore, a good first step would be to be able to classify a topic as controversial or not.

Looking at the definition of **controversy** from Werriam-Webster, we see: "a discussion marked especially by the expression of opposing views".

Thus, a topic whose daily polarity score is very stable throughout time would be considered not controversial, as around the same level of sentimental polarity is expressed each day. 
 Whereas a topic where the daily polarity score tends to swing between -1 and 1, can be considered as a topic where there is expression of opposing views or that a given view is expressed in a variety of way (alarmist against hopeful).

Therefore, examining the empirical variance of the daily average polarity score of a given topic seems like a reasonable heuristic.

This heuristic obviously assumes that there aren't consistently opposing views that cancel each other exactly the same day. This assumption tends to be hold, when looking at the data and its quantity.

Using our heuristic, we extracted the top 5 most polemic topics.

Polemic topics:

1. Wildfires
2. Deforestation
3. Ecosystem
4. Ozone
5. Nuclear

An example of a very negative quote around these topics is: "*Where a complaint alleges, knowing governmental action is affirmatively and substantially damaging the climate system in a way that will cause human deaths, shorten human lifespans, result in widespread damage to property, threaten human food sources and dramatically alter the planet's ecosystem, it states a claim for a due process violation to hold. Otherwise, it would be to say that the constitution affords no protection against a government's knowing decision to poison the air its citizens breathe or the water its citizens drink.*" by Ann Aiken, a United States District judge.

An example of a very positive quote is: "*While the agenda on climate change looks precarious with president elect Trump's picks of climate change skeptics and denialists. Latin america is heading in the opposite direction. In 2017, we expect to increasingly hear actors in the private sector multilateral development banks and civil society making the case for why action on climate change is needed for sustainable development. Countries from the region strongly back the Paris climate agreement and in November many announced plans to reduce emissions and promote renewable energy during the UN climate change conference in Marrakech. These efforts come as the region prepares to feel climate change's effects in increasingly tangible ways from drought in the Andes and the Amazon basin, to more powerful hurricanes in the Caribbean. As countries grapple with challenging growth forecasts for next year, leaders in 2017 may find opportunity in confronting climate change measures to improve energy efficiency. For example, it could help the region save billions of dollars annually and make businesses more competitive. Strong support for renewable energy, including solar and wind, could attract investment and reduce emissions. Meanwhile backing clean public transport can enhance mobility and productivity levels in cities, while preventing thousands of premature deaths from air pollution. In the Amazon, increasing modest investments to secure land rights for indigenous peoples could also significantly reduce emissions from deforestation and help protect vital ecosystems*" by Guy Edwards, a consultant focusing on climate change, geopolitics and Latin America.


As we can see from those two quotes, and it generalizes well to the rest of the corpus, quotes considered opposite by our sentimental polarity score tend to share a similar feeling: **Climate change is important and we need to act about it**. Indeed, the narrative around climate change can either alarmistic about the current situation or hopeful and positive about the actions taken.

When starting to look at this problem, we expected to see an opposition between a climate change skeptic narrative and a climate change alarmistic narrative. But, our findings don't back up our expectations. Either, the climate change skeptic narrative is actually much smaller than we think and it would be a case of a loud minority, or tools such as sentimental polarity and word embeddings are not the right tool to dissociate the two narratives.

But, our heurisitc is obviously as perfect as our filtering and we get some false positive such as this quote from Donald Trump: "The heart of the iran deal was a giant fiction that a murderous regime desired only a peaceful nuclear energy programme."

Non-polemic topics:

1. Earth
2. Climate
3. Gas
4. Sustainability
5. Energy




We tried extracting seasonality of the polarity time series or observing outliers events but nothing significant was found.



