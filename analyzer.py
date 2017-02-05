#!/usr/local/bin/python2

#################### IMPORTS #####################

import string
import pandas as pd
from nltk.corpus import stopwords

from dnnsent.sentiment import sentiment_score
from tokenizer import preprocess

from config import *

#################### CONFIG ######################

to_process = False
full = False

################### FUNCTIONS ####################


def process(series, full=False):

    # Preprocess data
    preprocessed = series.apply(preprocess)

    # Process stop words
    if full is True:
        stop = list(string.punctuation) + ['rt', 'via'] + stopwords.words('english')
    else:
        stop = list(string.punctuation) + ['rt', 'via']

    processed = preprocessed.apply(lambda x: [item for item in x if item.lower() not in stop])

    # Rejoin into string
    processed = processed.apply(lambda x: ' '.join(x))

    return processed


##################### MAIN #######################

# Read classified dataset
df = pd.read_csv(OUT_FILE)

if to_process:
    df['processed'] = process(df['Text'].astype(unicode), full)
else:
    df['processed'] = df['Text'].astype(unicode)

# Apply sentiment analysis
df['sentiments'] = df['processed'].apply(sentiment_score)
df.to_csv('predictions/' + user + '.csv')