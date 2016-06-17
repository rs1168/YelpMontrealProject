# Montrealer vs Montréalais:

A text-based comparison of Yelp restaurant reviews 
between English and French speakers in Montreal


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


###Results

<p class=MsoNormal style='text-indent:.5in;line-height:200%'>Of the 50 topics
found by the LDA model, we will examine those with the highest and lowest odds
ratios in our ordered logistic regression for each language.&nbsp; </p>

<div align=center>

<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=247
 style='width:247.0pt;border-collapse:collapse'>
 <tr style='height:22.25pt'>
  <td width=108 nowrap valign=top style='width:1.5in;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Topic</span></b></p>
  </td>
  <td width=139 nowrap valign=top style='width:139.0pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Odds Ratio coefficient</span></b></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 43: Recommendations</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>1962.63</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 17: </span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Rich and Decadent</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>605.2502</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 23:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Reading Menu</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>547.2684</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=247 nowrap colspan=2 valign=bottom style='width:247.0pt;border:
  none;border-bottom:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;
  height:30.0pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Table 1: Positive Topics, English</span></b></p>
  </td>
 </tr>
</table>

</div>

<p class=MsoNormal>&nbsp;</p>

<p class=MsoNormal style='text-indent:.5in;line-height:200%'>First we look at
the topics with the largest odds ratio coefficients in English found in Table
1.&nbsp; Topic 43 is associated with words about recommendations like <i>best,
ever, great, </i>and<i> recommend</i>.&nbsp; Topic 17 is associated with words
about “rich” foods like <i>duck, foie, gras, maple, syru,p</i> and<i> rich. </i>This
could mean that English reviews are most impressed by these kinds of foods.<i> </i>Topic
23 is associated with words about reading the menu such as <i>menu, will, read,
list, </i>and<i> yes</i>. </p>

<div align=center>

<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=247
 style='width:247.0pt;border-collapse:collapse'>
 <tr style='height:22.25pt'>
  <td width=108 nowrap valign=top style='width:1.5in;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Topic</span></b></p>
  </td>
  <td width=139 nowrap valign=top style='width:139.0pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Odds Ratio coefficient</span></b></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 3:&nbsp; </span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Bad Delivery Food </span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>.0017012</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 35:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Location</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>.0140399</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 15: </span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Bad Group Service</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>.0242154</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=247 nowrap colspan=2 valign=bottom style='width:247.0pt;border:
  none;border-bottom:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;
  height:30.0pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Table 2: Negative Topics, English</span></b></p>
  </td>
 </tr>
</table>

</div>

<p class=MsoNormal>&nbsp;</p>

<p class=MsoNormal style='text-indent:.5in;line-height:200%'>Next, we look at
the topics with the smallest odds ratio coefficients in English found in Table
2.&nbsp; Topic 3 is associated with words about poor quality delivery food like
<i>delivery, don’t, bad, food, and chinese</i>.&nbsp; The appearance of the
word <i>chinese</i> in the topic makes it seem that this topic referes to
Chinese food restaurants.&nbsp; Topic 35 is associated with words about
location like <i>st denis, st laurent, location, and elsewhere</i>.&nbsp; The
neighbhorshoods that appear in this topic are all major commercial arteries in
Montreal perhaps meaning that English reviews are not having good experiences
in those locations.&nbsp; Topic 15 is associated with words about poor service
but with relation to a group experience such as <i>us, food, service, asked,
and waiter, minutes</i>. </p>

<div align=center>

<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=247
 style='width:247.0pt;border-collapse:collapse'>
 <tr style='height:22.25pt'>
  <td width=108 nowrap valign=top style='width:1.5in;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Topic</span></b></p>
  </td>
  <td width=139 nowrap valign=top style='width:139.0pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Odds Ratio coefficient</span></b></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 16: </span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Dessert</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>29.04105</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 26:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Service/Ambiance</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>24.42117</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 25:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Positive Anecdote</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>21.05134</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=247 nowrap colspan=2 valign=bottom style='width:247.0pt;border:
  none;border-bottom:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;
  height:30.0pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Table 3: Positive Topics, French</span></b></p>
  </td>
 </tr>
</table>

</div>

<p class=MsoNormal>&nbsp;</p>

<p class=MsoNormal style='text-indent:.5in;line-height:200%'>Now we turn our
attention to the topics with the largest odds ratio coefficients in French
found in Table 3.&nbsp; Note that the words in the French topics are presented
in their stemmed form.&nbsp; Topic 16 is associated with words about dessert
like <i>thé, dessert, sucr, glac, </i>and<i> tart</i>.&nbsp; This could mean
that French reviews are most impressed by desserts and sweets.&nbsp; Topic 26
is associated with words about service a like <i>servic, agréabl, ambianc,
ador,</i>and<i> appréc</i>.&nbsp; Topic 25 is associated with words about a
positive anecdotal experience like <i>expérient, épic, cuisin, indien, coreen </i>and<i>
mang</i>.&nbsp; More precisely it seems that this topic is about trying out a
new kind of cuisine. </p>

<div align=center>

<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=247
 style='width:247.0pt;border-collapse:collapse'>
 <tr style='height:22.25pt'>
  <td width=108 nowrap valign=top style='width:1.5in;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Topic</span></b></p>
  </td>
  <td width=139 nowrap valign=top style='width:139.0pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  padding:0in 5.4pt 0in 5.4pt;height:22.25pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:#262626'>Odds Ratio coefficient</span></b></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 29:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Service</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>.0031253</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 49:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Poor Service</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid #D9D9D9 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>.0089967</span></p>
  </td>
 </tr>
 <tr style='height:30.0pt'>
  <td width=108 style='width:1.5in;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Topic 0:</span></p>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Negative Anecdote</span></p>
  </td>
  <td width=139 style='width:139.0pt;border:none;border-bottom:solid windowtext 1.0pt;
  padding:0in 5.4pt 0in 5.4pt;height:30.0pt'>
  <p class=MsoNormal><span style='font-size:10.0pt;font-family:Arial;
  color:#1C639E'>.0232125</span></p>
  </td>
 </tr>
 <tr style='height:27.85pt'>
  <td width=247 nowrap colspan=2 valign=bottom style='width:247.0pt;border:
  none;border-bottom:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;
  height:27.85pt'>
  <p class=MsoNormal><b><span style='font-size:10.0pt;font-family:Arial;
  color:gray'>Table 4: Negative Topics, French</span></b></p>
  </td>
 </tr>
</table>

</div>

<p class=MsoNormal>&nbsp;</p>

<p class=MsoNormal style='text-indent:.5in;line-height:200%'>Finally, we look
at the topics with the smallest odds ratio coefficients in French found in
Table 4.&nbsp; Topic 29 is associated with words about service like <i>servic, command,
serveur, attent, </i>and<i> minut</i>.&nbsp; Since the coefficient is very
small, it is reasonable to think that this corresponds to bad service.&nbsp; Topic
49 is associated with words more explicitly about bad service a like <i>non, rien,
plus, servic,</i>and<i> demand</i>.&nbsp; The appearance of yet another topic
related to service and its large impact on star rating highlights the
importance of service to French commenters.&nbsp; Topic 0 is appears to be associated
with words about a negativee anecdotal experience like <i>plus, jam[ais], vrai,
famill, arriv </i>and<i> mang</i>.</p>

<p class=MsoNormal><span style='font-size:20.0pt'>&nbsp;</span></p>

###Conclusion

<p class=MsoNormal>&nbsp;</p>

<p class=MsoNormal style='text-indent:.5in;line-height:200%'>Using our LDA
model, we have shown what users care about most in their reviews of
restaurants.&nbsp; Overall it seems that French commenters care about dessert
and service while English commenters care about making recommendation, whether
positive or negative, and specific kinds of “rich” food.&nbsp; From the topics
we extracted, we predicted star rating using an ordered logistic regression
model.&nbsp; In future work, it would be interesting to apply a bigram LDA and
analyze these bigram topics in a similar fashion as the unigram topics in this
paper.</p>

