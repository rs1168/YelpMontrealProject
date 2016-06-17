'''
Yelp Montreal restaurant LDA Analysis

by Richard Sequeira
'''
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.stem import snowball
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.snowball import FrenchStemmer
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
import gensim

tokenizer = RegexpTokenizer(r'\w+')


###English Data Set###
doc_set_en = english_df['text']

en_stop = get_stop_words('en')

p_stemmer = EnglishStemmer()

from pandas import Series
doc = Series.tolist(doc_set_en)
texts=[]

for i in doc:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    
    # add tokens to list
    texts.append(stopped_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# limit to the 10000 most common words    
dictionary.filter_extremes(keep_n=10000)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel= gensim.models.ldamodel.LdaModel(corpus, num_topics=50, id2word = dictionary, passes=20)

#print
ldamodel.print_topics(num_topics=50, num_words=10)

###FRENCH###
doc_set_fr = french_df['text']

fr_stop = get_stop_words('fr')

f_stemmer = snowball.FrenchStemmer()

from pandas import Series
doc_fr = Series.tolist(doc_set_fr)
texts_fr=[]

for j in doc_fr:

    # clean and tokenize document string
    raw_fr = j.lower()
    tokens_fr = tokenizer.tokenize(raw_fr)

    # remove stop words from tokens
    stopped_tokens_fr = [j for j in tokens_fr if not j in fr_stop]
    stopped_tokens_fr2 = [j for j in stopped_tokens_fr if not j in en_stop]


    # stem tokens
    stemmed_tokens_fr = [f_stemmer.stem(j) for j in stopped_tokens_fr2]
 
    
    # add tokens to list
    texts_fr.append(stemmed_tokens_fr)
    

# turn our tokenized documents into a id <-> term dictionary    
dictionary_fr = corpora.Dictionary(texts_fr)

# limit to the 10000 most common words 
dictionary_fr.filter_extremes(keep_n=10000)

# convert tokenized documents into a document-term matrix
corpus_fr = [dictionary_fr.doc2bow(text_fr) for text_fr in texts_fr]

# generate LDA model
ldamodel_fr = gensim.models.ldamodel.LdaModel(corpus_fr, num_topics=50, id2word = dictionary_fr, passes=20)

#print
ldamodel_fr.print_topics(num_topics=50, num_words=10)


###English extraction of topic distribution
lda_corpus= lda_en[corpus]
topic_vector = []

###Get topic distribution theta
for i in range(0, 44534):
    topic_vector.append(ldamodel[corpus[i]])


###Extracting distributions
probmatrix=[]
for i in topic_vector:
    tmp= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for j in i:
        tmp[j[0]] = j[1]
    probmatrix.append(tmp)

import pandas as pd
Document_TopicProbMatrix_en =pd.DataFrame(probmatrix)

###English Dataframe with thetas
EN_DocTPM = pd.concat([english_df, Document_TopicProbMatrix_en], axis=1)


###French Extraction extraction of topic distribution
topic_vector_fr = []

###get topic distribution values
for i in range(0, 6759):
    topic_vector_fr.append(ldamodel_fr[corpus_fr[i]])

###Extracting distributions
probmatrix_fr=[]
for i in topic_vector_fr:
    tmp= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for j in i:
        tmp[j[0]] = j[1]
    probmatrix_fr.append(tmp)

import pandas as pd
Document_TopicProbMatrix_fr =pd.DataFrame(probmatrix_fr)

###French Dataframe with thetas
FR_DocTPM = pd.concat([french_df, Document_TopicProbMatrix_fr], axis=1)







