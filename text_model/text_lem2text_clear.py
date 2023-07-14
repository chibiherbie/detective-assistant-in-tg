# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:42:13 2023
clear of stopwords

"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import nltk
import re
nltk.download('stopwords')


class text_lem2text_clear(BaseEstimator, TransformerMixin):
    def __init__(self):
        return

    def fit(self, X, y=None):
        stop_words = nltk.corpus.stopwords.words('russian')
        self.stop_words = set(stop_words)
        return self

    def transform(self, X):
        X['clr_text'] = X['lem_text'].apply(self.clear_string)

        return X

    def clear_string(self, s):
        s = s.replace('.', '')
        s = s.replace(',', '')
        s = s.replace("'", ' ')
        s = s.replace('"', ' ')
        s = s.replace('-', ' ')
        s = s.replace('+', ' ')
        s = s.replace('/', ' ')
        s = s.replace('ё', 'е')
        tokens = s.split(sep=' ')
        tokens = [w for w in tokens if not w.lower() in self.stop_words]
        tokens = [w for w in tokens if not w.isnumeric()]
        tokens = ' '.join(tokens)
        return tokens


if __name__ == '__main__':
    df = pd.read_excel('Data_lem.xlsx')
    transformer = text_lem2text_clear()
    transformer = transformer.fit(df)
    df1 = transformer.transform(df)
    df1.to_excel('Data_clear.xlsx', index=False)
