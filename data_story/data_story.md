# Polarization around climate change: 
## Is it growing as fast as the polar circle is shrinking? 

## Abstract:
As the effects of climate change become increasingly visible in our daily life, it is time for humanity to come together for a joint effort to come back to an equilibrium with nature. A joint effort requires collaboration and agreement on what climate change is and what we should do. In this data story, we will study the polarization of opinions around climate change that tend to make this collaboration difficult to accomplish and examine its dynamics. This will be done through the lens of Quotebank, an open corpus of 178 million quotations
attributed to the speakers who uttered them, extracted from 162 million English news articles published between 2008 and 2020.


## From Quotebank to quotes about climate

What are we working with? Quotes, about climate.
Weeeell actually to be precise it's quotes that contain a word from vocabulary that revolves around climate issues, for example "energy" or "typhoon" or "agriculture". But "The Rolling Stones play with such energy" does not talk about climate at all right? This is a false positive (FP): naïvely looks like a climate quote, but really isn't. There will always be some FP, but too much is a problem as it would discrit any further result. We some strict filtering to reduce our rate of FPs, at the cost of loosing true positives of course. This still seemed like the right way to go. Notable trouble makers where "energy" or "atmosphere", that oftentimes are used in an abstract way.

In addition of the quotes, we also have the speaker's name, the date they said or wrote the quote, and the number of times this quote has been in a quotebank article.

We end up with XXX quotes from XXX different speakers, quoted between 2015 and 2020. The most viral of which is unfortunately a FP although it contains both "environment" and "climate" : YYYY

## Who talks about climate ?

Have you ever wondered who are the most influencial ecologists? Do news articles prefer to quote scientists? Politicians? Greta Thunberg? Who says the most viral punchlines?
We did!

### Climate quote influence podium
Who doesn't like a good old podium? Even better, a dynamic and continous podium. A podium of the most influencial speakers. To measure "influence", we use the number of times a speaker has been quoted in times, all climate quotes considered.

<embbed bar race>

And our best contenders are:
<copy md from speakers nb>

### Virality dependence of influence
If you want to be on the podium, it looks like having a few viral quotes is not enough to do the trick. The following graph shows that for our most quoted speakers, even their most famous quote is rather unnimpressive. In the meantime, many of the punchliners -that's how we'll name speakers with very famous quotes- are aren't quoted a whole lot when cumulated. This is seen by the proximity of our point to the 1:1 line.

### Expending the dataset : scraped feature
##### Gender of the speakers

##### Age of the speakers

##### Political party of the speaker

### Word embedding 
Juste technique pour avoir de spoints par feature ==> feature pour speaker

### Clustering 
Now that we have various ways to identify our speakers, and how each of them speak, we can look for similarities and disparities between speakers, and how we can explain them. (TODO maybe redondant avec des parties du dessus l'intro de cette partie). 
Humans like to categorize, and we are humans, so let's go. We can cluster our speakers based on their speach-print, their word embeddings. Using KMeans, word embeddings of speakers cluster in the following way. 

<embbed plain Scatterplot>

Yes nice, but what about it? 
Ideally, we would expect that different kinds of people speak differently, and that this clustering gives us 4 "personnas", robot portraits of who speaks in this way rather then that. Of course, the world is not ideal, but sometimes we get lucky. To characterise a cluster, we look at speakers closest to its center. In doing so we identify two clusters with pretty defined traits:
- The US politician
- The Indian

<Embbed scatterplot with pictures or other viz with pictures of 10 speakers>

##### Profil type



## How do we speak about climate ? The fine details of its narrative in the news

### Feature de polarization

### Evolution of polarization

Relativement constant (mean, std)

### Polemic topics (time series analysis bb)

Which topic is important to which wing. Topic pour lequel chaque wing est polarisé. 

### Semantic separation (ANTOINE)

Distance sémantique entre les groupes (certaines stagnent, diminuent et d'autres augments). Essayer d'avoir GIF avec PCA constantes et PSNE

## Bonus : Input et regarde à qui tu ressembles hihi potit blaugueur



Requirement de fin :

- s'accorder sur la palette : **magma**
- s'accorder sur les tailles de figure
- mettre les titres/ labels en fontsize corrects
- clean les notebook 
- save toutes les images avec $\geq 300$ dpi
plt.savefig(filname, dpi=300)





