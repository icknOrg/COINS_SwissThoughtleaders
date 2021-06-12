# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 15:37:45 2021

@author: Johanna
"""

import warnings
warnings.filterwarnings("ignore")
import numpy as np 
import pandas as pd 
import unidecode

import re 
from add_sentiment import process_summary
import tensorflow as tf
import ktrain 
from ktrain import text 

from nltk import word_tokenize 
from nltk.tokenize import treebank
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#get training and test data
data_train = pd.read_excel('authors_train.xlsx', index_col=0, dtype=str)
data_test = pd.read_excel('authors_test.xlsx', index_col=0, dtype=str)

data_train = data_train.drop(columns=['title', 'media', 'weight', 'date', 'desc', 'summary', 'link', 'flag'])
data_test = data_test.drop(columns=['title', 'media', 'weight', 'date', 'desc', 'summary', 'link', 'flag'])

#data_train['Processed_summary'] = data_train['Processed_summary'].str.replace('\d+', '')
#data_test['Processed_summary'] = data_test['Processed_summary'].str.replace('\d+', '')

print("Size of train dataset: ",data_train.shape)
print("Size of test dataset: ",data_test.shape)

data_train= data_train.dropna()
data_test= data_test.dropna()
#return multiple tuples, 1 for training, 1 for test, and preprocess data
(X_train, y_train), (X_test, y_test), preprocess = text.texts_from_df(
                    train_df = data_train,
                    text_column = 'Processed_summary',
                    label_columns = 'sentiment',
                    val_df = data_test,
                    maxlen = 400,
                    preprocess_mode = 'bert')


model = text.text_classifier(name = 'bert',
                             train_data = (X_train, y_train),
                             preproc = preprocess)

#batch size 6 is recommended with a maxlen to 500
learner = ktrain.get_learner(model=model, train_data=(X_train, y_train),
                   val_data = (X_test, y_test),
                   batch_size = 6)

predictor = ktrain.get_predictor(learner.model, preprocess)
predictor.save('/content/bert')

#sample dataset to test on 
#Muschg_all_2021
data = pd.read_excel('Muschg_all_2021.xlsx', index_col=0, dtype=str)
#data = process_summary(data)

#Preprocessing 
process_summary(data)
# 
data = data[data.Processed_summary != 'nan']
data = data.drop(columns=['title', 'media', 'date', 'desc', 'summary', 'link', 'flag'])

data = data.Processed_summary.tolist()

#give the prediction probabilty for each class
predictor.predict(data, return_proba=True)

#output of different classes
#.get_classes()

#saving the model and weights, laoding model and predicting data
# predictor.save('/content/bert')
# predictor_load = ktrain.load_predictor('/content/bert')
# predictor_load.predict(data)

