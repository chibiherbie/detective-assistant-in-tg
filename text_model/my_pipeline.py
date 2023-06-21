# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 00:33:05 2023


"""

from sklearn.pipeline import Pipeline
from text_clear2vect import vectorizer
from model import my_model
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib


def test_model_linear(df, labels, param_grid, n_iter=5):
    #функция производит перебор параметров по схеме решетчатого поиска, запоминает 
    #наилучшие параметры и возыращает результат
    X=df['clr_text']
    fl_rez=0
    Stat=[]
    it=0
    n_it=(len(param_grid['vectorizer__method'])*
          len(param_grid['vectorizer__min_df'])*
          len(param_grid['vectorizer__max_df'])*
          len(param_grid['vectorizer__ngram_range'])*
          len(param_grid['model__name_model'])*n_iter
          
          )
    
        
    for vectorizer__method in param_grid['vectorizer__method']:
        for vectorizer__min_df in param_grid['vectorizer__min_df']:
            for vectorizer__max_df in param_grid['vectorizer__max_df']:
                for vectorizer__ngram_range in param_grid['vectorizer__ngram_range']:
                    for model__name_model in param_grid['model__name_model']:
                        for i in range(n_iter):
                            
                            try:
                                pipe = Pipeline([("vectorizer", vectorizer(method=vectorizer__method,
                                                  min_df=vectorizer__min_df,
                                                  max_df=vectorizer__max_df,
                                                  ngram_range=vectorizer__ngram_range)),
                                         
                                         ('model', my_model(name_model=model__name_model))
                                         ])
                                X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, stratify=labels)
                                pipe.fit(X_train, y_train)
                                score=pipe.score(X_test, y_test)
                                stat=[vectorizer__method,vectorizer__min_df,vectorizer__max_df,
                                      vectorizer__ngram_range, model__name_model, i,score ]
                                Stat.append(stat)
                            except:
                                raise RuntimeError('''problem with params: vectorizer__method-{},
                                                   vectorizer__min_df-{},
                                                   vectorizer__max_df-{},
                                                   vectorizer__ngram_range-{},
                                                   model__name_model-{},
                                                   iter-{}''',format(vectorizer__method,vectorizer__min_df,
                                                   vectorizer__max_df,vectorizer__ngram_range,model__name_model,
                                                   i))
                                return False
                            it+=1
                            now=int(it*100/n_it)
                            if (now%5)==0:
                                print('{0}% completed, '.format(now))
                            
                                
            
            
            
            
            
    Stat=pd.DataFrame(Stat, columns=['vectorizer__method','vectorizer__min_df','vectorizer__max_df',
                                     'vectorizer__ngram_range','model__name_model', 'runs', 'score' ])
    return Stat

if __name__ == '__main__':
    df=pd.read_excel('Data_clear.xlsx')
   
    labels=df['labels']
    
    
    
    param_grid = {'vectorizer__method': [ 'bw'],
                  'vectorizer__min_df': [0, 0.001, 0.01, 0.02,0.05],
                  'vectorizer__max_df': [0.8, 0.85, 0.9, 0.95, 0.98,1.],
                  'vectorizer__ngram_range': [(1,1), (1,2), (1,3)],
                  'model__name_model': ['LR', 'RFC', 'GBC', 'MLPClassifier']
                  
                    }
    
    rez=test_model_linear(df, labels, param_grid=param_grid, n_iter=5)
    try:
        rez.to_excel('stat_rez_runs.xlsx')
    except:
        raise RuntimeError('error of file saving ')
    
    rez1=rez.groupby(['vectorizer__method', 'vectorizer__min_df', 'vectorizer__max_df',
            'vectorizer__ngram_range', 'model__name_model'])['score'].mean()
    rez1=rez1.reset_index()
    rez1.to_excel('stat_rez.xlsx')
    ind=rez1['score'].argmax()
    params_model={}
    params_model['vectorizer__method']=rez1['vectorizer__method'].iloc[ind]
    params_model['vectorizer__min_df']=rez1['vectorizer__min_df'].iloc[ind]
    params_model['vectorizer__max_df']=rez1['vectorizer__max_df'].iloc[ind]
    params_model['vectorizer__ngram_range']=rez1['vectorizer__ngram_range'].iloc[ind]
    params_model['model__name_model']=rez1['model__name_model'].iloc[ind]
    
    
    
    print('best params: ', params_model)
    print('best score: ', rez1['score'].iloc[ind])
    
    pipe_model=Pipeline([("vectorizer", vectorizer(method=params_model['vectorizer__method'],
                      min_df=params_model['vectorizer__min_df'],
                      max_df=params_model['vectorizer__max_df'],
                      ngram_range=params_model['vectorizer__ngram_range'])),
             
             ('model', my_model(name_model=params_model['model__name_model']))
             ])
    X=df['clr_text']
    pipe_model.fit(X, labels)
    joblib.dump(pipe_model, 'model_nlp.pkl')
    
    