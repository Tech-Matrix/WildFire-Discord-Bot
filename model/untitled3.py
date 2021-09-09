# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c0eBWOAnk3VlsKF3FfLxWc1HaXM-xdtu
"""

import re
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
import pickle
import nltk
from sklearn.model_selection import train_test_split
nltk.download('rslp')
nltk.download('stopwords')
def function(text):
  
  

  dt_train = pd.read_csv(r"train_tweet.csv", encoding="ISO-8859-1")
  dt_train = dt_train.drop(labels = ['id'], axis = 1)
  dt_train['len'] = dt_train['tweet'].str.len()
  l=np.array([text])
  stemmer = nltk.stem.RSLPStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  corpus = []
  corpus1=[]
  for tweet in dt_train['tweet'].values:
    review = re.sub(r"@[A-Za-z0-9_]+", " ", tweet)
    review = re.sub('RT', ' ', review)
    review = re.sub(r"https?://[A-Za-z0-9./]+", " ", review)
    review = re.sub(r"https?", " ", review)
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(all_stopwords) if len(word) > 2]
    review = ' '.join(review)
    corpus.append(review)
  corpus = np.array(corpus)
  for tweet in l:
    review = re.sub(r"@[A-Za-z0-9_]+", " ", tweet)
    review = re.sub('RT', ' ', review)
    review = re.sub(r"https?://[A-Za-z0-9./]+", " ", review)
    review = re.sub(r"https?", " ", review)
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(all_stopwords) if len(word) > 2]
    review = ' '.join(review)
    corpus1.append(review)
  corpus1 = np.array(corpus1)
  c_train = corpus
  y = dt_train['label']
  X_train, X_test, y_train, y_test = train_test_split(c_train, dt_train['label'], test_size=0.33, random_state=0)
  tweet_tokenizer = TweetTokenizer() 
  vectorizer = CountVectorizer(analyzer="word", tokenizer=tweet_tokenizer.tokenize, max_features = 1010)
  X_train = vectorizer.fit_transform(X_train).toarray()
  X_test= vectorizer.transform(X_test).toarray()
  c = vectorizer.transform(corpus1).toarray()
  filename = 'finalized_model.sav'
  loaded_model = pickle.load(open(filename, 'rb'))
  
  s=loaded_model.predict(c)
  if s[0]==0:
    print("non offensive")
  else:
    print("offensive")
  
text = "fvck that depression"
function(text)