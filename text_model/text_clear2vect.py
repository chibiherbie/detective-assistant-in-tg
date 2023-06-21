# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:42:13 2023


"""

import pandas as pd

from sklearn.decomposition import LatentDirichletAllocation

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin


class vectorizer(BaseEstimator, TransformerMixin):
    def __init__(self,  method='bw', min_df=2, max_df=1.0, ngram_range= (1,1), LDA_n_components=10, LDA_n_lexems=10  ):
        """
        method - способ векторизации текста: bw - мешок слов, tfidf - tfidf
        LDA - латентное распределение Дирихле
        min_df - используется в методе bw, tfidf. Параметр определят больше скольки 
                    раз должно встречаться слово во всех корпусах, что бы 
                    оно было добавлено в словарь
        max_df - аналогично bw_min_df только в другую сторону
        LDA_n_components - количество тем в LDA
        LDA_n_lexems - количество лексем в теме
        self.model - основная модель
        self.model_bw - используется как этап расчета в LDA
        self.ngram_range - параметр ngram_range  в bw и tfidf
        
                    
        
        """
        self.method=method
        self.min_df=min_df
        self.max_df=max_df
        self.ngram_range=ngram_range
        self.LDA_n_components=LDA_n_components
        self.LDA_n_lexems=LDA_n_lexems
        return
    
    def fit(self, X, y = None):
        """
        Изучает правила преобразования на основе входных данных X.
        """
        
        if self.method=='tfidf':
            model = TfidfVectorizer(min_df=self.min_df, max_df=self.max_df, ngram_range=self.ngram_range)
            model = model.fit(X)
            
        elif self.method=='bw':
            model = CountVectorizer(min_df=self.min_df, max_df=self.max_df, ngram_range=self.ngram_range)
            model = model.fit(X)
            
            
            
        else:
            raise RuntimeError('unknown of method name')
            return
        
        self.model=model
        return self


    def transform(self, X):
        """
        Преобразует X в новый набор данных Xprime и возвращает его.
        """
        
        if self.method=='tfidf':
            
            values = self.model.transform(X)
            # Show the Model as a pandas DataFrame
            feature_names = self.model.get_feature_names_out()
            df_rez=pd.DataFrame(values.toarray(), columns = feature_names)
        elif self.method=='bw':
            
            bag_of_words =self.model.transform(X)
            
            feature_names = self.model.get_feature_names_out()
            df_rez=pd.DataFrame(bag_of_words.toarray(), columns = feature_names)
            
        
        
        else:
            raise RuntimeError('unknown of method name')
            return
        return df_rez
        
if __name__ == '__main__':
    df=pd.read_excel('Data_clear.xlsx')
    vect=vectorizer(method='bw', min_df=0.0, max_df=0.9, ngram_range=(1,1))
    Result=df['clr_text']
    vect=vect.fit(Result)
    df1=vect.transform(Result)
    df1['labels']=df['labels']
    df1.to_excel('Data_vect.xlsx',index=False )
    
    
    

            
    
