# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:42:13 2023

Transform text to adaptive text

"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import nltk
import string
nltk.download('punkt')


class text2tokenize_text(BaseEstimator, TransformerMixin):
    def __init__(self):
        return

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['tokenize_text'] = X['text'].apply(self.tokenize_string)
        return X

    def tokenize_string(self, s):
        # firstly let's apply nltk tokenization
        tokens = nltk.word_tokenize(s)

        # let's delete punctuation symbols
        tokens = [str.lower(i) for i in tokens if (i not in string.punctuation)]

        tokens = ' '.join(tokens)
        return tokens


if __name__ == '__main__':
    # nltk.download("stopwords")
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')
    # stopwords = nltk.corpus.stopwords.words('Turkish')

    df = pd.read_excel('data.xlsx')
    df = df[['text', 'labels']]
    df = df.dropna()
    transformer = text2tokenize_text()
    transformer = transformer.fit(df)
    df1 = transformer.transform(df)
    df1.to_excel('Data_token.xlsx', index=False)
