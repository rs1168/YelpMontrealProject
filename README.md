# YelpMontrealProject

##Abstract

In this paper, we examine how English and French Yelp restaurant reviews differ in Montreal.  We use the open dataset from the Yelp Dataset Challenge with over 50,000 reviews from Montreal.  With access to the actual text of Yelp reviews, we have a somewhat novel opportunity to analyze how subjective perceptions of a restaurant experience combined with Yelp users’ language inform review star rating.  To find latent topics from the reviews for each language, we use Latent Dirichlet Allocation, then we analyze the relationship between these topics and review star rating.

###Introduction

Yelp ratings have been shown to have a large effect on the success of businesses.  A study looking at star rating and restaurant reservations found that “an extra half-star rating causes restaurants to sell out 19 percentage points more frequently, with larger impacts when alternate information is more scarce” [1].  Another study looking at the relationship between star rating and restaurant revenue found that “a one-star increase in Yelp rating leads to a 5 to 9 percent increase in revenue” [2].

The question is: how can a restaurant identify the what its customers care about from a large body of reviews? And on top of that, what if a restaurant is serving a multilingual clientele?  Using Montreal as an example of this situation, our goal is to identify what English language users compared to French language users care about most when leaving a review.
	
In order to condense the reviews into more interpretable data, we use the Latent Dirichlet Allocation (LDA) model to classify each review word’s likely topic.  Some topics that were extracted include service, value, food, price, and ambience.  Then using ordered logistic regression, we identify the topics that have the greatest impact on review star rating. 

###Related Work

There are a variety of topic models for text data.  Latent Semantic Indexing is one most closely related with dimensionality reduction.  LSI is more precisely an information retrieval technique the uses singular value decomposition to identify patterns in the relationships between the terms and “concepts” contained in a collection of text [3].  Hoffman improved upon this model with a generative probabilistic model called Probabilistic Latent Semantic Indexing however it potentially has issues with overfitting when applied to small datasets [4][5]. 

Biel et al. first proposed LDA as an improvement on Hofmann’s PLSI model [5].  We used the Latent Dirichlet Allocation model to approach the clustering of topics for the Yelp restaurant review text since LDA is one of the most widely-used methods for general text classification.  While generative models are often used to predict new observations given an underlying distribution, in this paper we do the opposite and use LDA to perform latent factor analysis.  

The winning entry in the 2013 Yelp Dataset Challenge by Huang et al. focused on identifying topics in reviews which are important to the user, referring to criteria other than quality of food [6].  They implemented LDA using the online LDA algorithm proposed by Hoffman [7].  While we do not replicate this work, the attention it received suggests that using an LDA model is reasonable. 

###Methodology

We obtained the data as three JSON files which contain information about businesses, users, and reviews from the cities made available through the Yelp Dataset Challenge.  Each business includes information about the type of business, location, rating, categories, business name, and a unique id.  Every user includes review count, average rating, and a unique id.  Finally, each review has a rating, review text, and is associated with a specific business id and user id.  
All of the data manipulation is performed using R.  First we convert each of the JSON files into an R data frame object.  We limit the business data frame to those businesses located in Montreal.  Next, we limit the business data frame to those businesses whose type include “restaurant”.   

Then, we include the information in the business data frame in the reviews data frame, merging on business_id.  Likewise, we include information from the user data frame in the review data frame, merging on user_id.  The resulting data frame is one where each review constitutes an observation.  We use the Textcat package in R to detect the language of each review and split the data frame by English and French comments.  We drop reviews of any other languages.  We are left with 44,534 reviews across 2,998 restaurants in English and 6,759 reviews across 2,048 restaurants in French.

Our variables of interest were stars which is the discrete number of stars given by each review, ranging from one to five and text which was the text within each review. 

Finally, we transfer our data to Python and begin our latent topic analysis for Montreal using the Genism library.  For the English data frame, we construct a corpus from its review texts, and restricting our dictionary to only the 10,000 most common words after stopword removal.  We experimented with Porter’s Snowball Stemmer in the Natural Language Toolkit library, but we found that having an appropriate stopword list gave much more interpretable results.  For the French data frame, we follow the same steps as with the English data frame except we do implement Porter’s Snowball Stemmer using the French language stemmer.

In order to find the most appropriate number of topics k, we run the model using different values of k, ranging from 10 to 100.   Based on the selection process proposed by Huang et al., we inspect each of the words associated with each generated topic and settled on k = 50 since it had what appears to be the most informative and reasonable topics [6].  Although a few of the topics have meanings that are ambiguous, the vast majority have clear interpretations.

We obtain the topic distribution for each review in both data frames from the LDA models and add 50 columns with the probability that a given review is about that topic.  These topic probabilities are the independent variables and stars is the dependent variable in our statistical analyses.  We chose to perform an ordered logistic regression.  An OLS regression analysis is problematic in this case because the assumptions of OLS are violated by the discrete ordinal nature of the dependent variable stars.  
