import pickle
import re
from pathlib import Path

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

nltk.download('rslp')
nltk.download('stopwords')

filename = Path("model", "finalized_model.sav")
loaded_model = pickle.load(filename.open(mode="rb"))

all_stopwords = stopwords.words('english')
all_stopwords.remove('not')


def clean_content(content: str) -> list:
    review = re.sub(r"@[A-Za-z0-9_]+", " ", content)
    review = re.sub('RT', ' ', review)
    review = re.sub(r"https?://[A-Za-z0-9./]+", " ", review)
    review = re.sub(r"https?", " ", review)
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    return review.split()


def generate_corpus(text):
    corpus1 = []
    for tweet in np.array([text]):
        review = clean_content(tweet)
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(all_stopwords) if len(word) > 2]
        review = ' '.join(review)
        corpus1.append(review)

    return np.array(corpus1)


def predict(vectorizer, content: str):
    c = vectorizer.transform(generate_corpus(content)).toarray()

    s = loaded_model.predict(c)
    if not s[0]:
        return False
    return True

    # if s[0] == 0:
    #     print("non offensive")
    # else:
    #     print("offensive")


def train() -> CountVectorizer:
    dt_train = pd.read_csv(Path("model", "train_tweet.csv"), encoding="ISO-8859-1")
    dt_train = dt_train.drop(labels=['id'], axis=1)
    dt_train['len'] = dt_train['tweet'].str.len()
    stemmer = nltk.stem.RSLPStemmer()
    corpus = []

    for tweet in dt_train['tweet'].values:
        review = clean_content(tweet)
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(all_stopwords) if len(word) > 2]
        review = ' '.join(review)
        corpus.append(review)
    corpus = np.array(corpus)

    c_train = corpus

    x_train, x_test, _, _ = train_test_split(c_train, dt_train['label'], test_size=0.33, random_state=0)

    tweet_tokenizer = TweetTokenizer()
    vectorizer = CountVectorizer(analyzer="word", tokenizer=tweet_tokenizer.tokenize, max_features=1010)
    vectorizer.fit_transform(x_train).toarray()
    vectorizer.transform(x_test).toarray()

    return vectorizer
