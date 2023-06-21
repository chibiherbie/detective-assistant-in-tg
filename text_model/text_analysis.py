# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:15:30 2023

@author: Leonid
"""


from sklearn.pipeline import Pipeline
from text_clear2vect import vectorizer
from model import my_model
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from docx import Document

from text2tokenize_text import text2tokenize_text
from text_tokenize2text_lem import text_tokenize2text_lem
from text_lem2text_clear import text_lem2text_clear
import nltk
import re



class text_analysis_class:
    def __init__(self,pipe_mode, measure_unit):
        #формируем конвеер
        # self.pipe= Pipeline([("tokenizer",text2tokenize_text()),
        #                      ("lematizer",text_tokenize2text_lem()),
        #                      ("clearaizer",text_lem2text_clear()),
        #                      ('pipe_model', pipe_model) 
        #                      ])
        self.pipe=pipe_model
        
        self.tokenizer=text2tokenize_text()
        self.tokenizer.fit(None)
        
        self.lematizer=text_tokenize2text_lem()
        self.lematizer.fit(None)
        
        self.clearaizer=text_lem2text_clear()
        self.clearaizer.fit(None)
        
        self.tokenizer_p=re.compile(r'(?<=\w[.!?]) ')
        self.measure_unit=measure_unit
        return
    
    def text2samples(self, text):
       list_tokens=self.tokenizer_p.split(text)
       list_tokens=pd.Series(list_tokens)
       df=pd.DataFrame({'text':list_tokens})
       return df
   
    def labels2measure(self, s):
        try:
            return self.measure_unit[s]
        except:
            raise RuntimeError('error of measure to unit: {0}'.format(s))
        return ''
    def get_stat(self, clr_text):
        
        rez_s=''
        flag=False
        for s in clr_text:
            if flag==False:
                rez_s=s
                flag=True
            else:
                rez_s+=' '+s
                
        tokens=rez_s.split(sep=' ')
        tokens=pd.Series(tokens)
        
        return tokens.value_counts()    
    
    def predict(self, text):
        
        
        #text to samples
        df=self.text2samples(text)
        
        #tokenaiz
        df1=self.tokenizer.transform(df)
        
        #lematize
        df1=self.lematizer.transform(df1)
        
        #clear
        df1=self.clearaizer.transform(df1)
        
        
        y_pred=self.pipe.predict(df1['clr_text'])
        df1['labels']=y_pred
        df1['measure']=df1['labels'].apply(self.labels2measure)
        
        stat=self.get_stat(df1['clr_text'])
        return df1, stat
        


if __name__=='__main__':
    
    pipe_model = joblib.load('model_nlp.pkl')
    
        
    document = Document('text.docx')
    text=''''''
    flag=False
    for p in document.paragraphs:
        if flag==False:
            text=p.text
            flag=True
        else:
            text+=' \n '+p.text
    
    measure_unit=pd.read_excel('measure_unit.xlsx')
    measure_unit.set_index('unit_of_measurement', inplace=True)
    measure_unit=measure_unit['measure']
    model=text_analysis_class(pipe_model, measure_unit)
    df_rez, stat=model.predict(text)
    try:
        df_rez.to_excel('text_analysis_result.xlsx')
        stat.to_excel('text_analysis_result_stat.xlsx')
    except:
        raise RuntimeError('Error of file saving. Close files: "text_analysis_result" and "test_analyses_result_stat", please')
    