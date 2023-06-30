# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 23:09:12 2023


"""

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier as KNC

from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import f1_score

import pandas as pd
from sklearn.model_selection import train_test_split


class my_model(BaseEstimator, TransformerMixin):
    def __init__(self, name_model='LR'):
        self.name_model = name_model

        return

    def fit(self, X, labels=None, ):

        if self.name_model == 'LR':
            lr = LogisticRegression(max_iter=1000)
        elif self.name_model == 'LinearSVC':
            lr = LinearSVC()
        elif self.name_model == "MLPClassifier":
            lr = MLPClassifier(max_iter=1000, hidden_layer_sizes=(100, 100, 50), solver='adam',
                               activation='relu')
        elif self.name_model == "SVC":
            lr = SVC()
        elif self.name_model == "KNC":
            lr = KNC()
        elif self.name_model == "RFC":
            lr = RFC()
        elif self.name_model == "GBC":
            lr = GBC()

        else:
            print("unknown model")
            return False

        lr = lr.fit(X, labels)
        self.model = lr

        return self

    def predict(self, X):

        y = self.model.predict(X)
        return y

    def score(self, X, y=None):

        X_out_pred = self.model.predict(X)
        return f1_score(y, X_out_pred, average='macro')


if __name__ == '__main__':
    df = pd.read_excel('Data_vect.xlsx')

    # тестируем на линейной моделе
    labels = df['labels']

    del df['labels']
    # model=my_model(name_model='MLPClassifier')
    # X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.3, stratify=labels, random_state=42)
    # model.fit(X_train, y_train)
    # score=model.score(X_test, y_test)
    # print(score)

    # тестируем на k-nn моделе
    model = my_model(name_model='RFC')
    X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.3, stratify=labels, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(score)
