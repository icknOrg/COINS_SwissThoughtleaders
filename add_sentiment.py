# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:14:37 2021

@author: Johanna
"""

"""
SentiWS is licensed under a Creative Commons Attribution-Noncommercial-Share Alike 3.0 
Unported License (http://creativecommons.org/licenses/by-nc-sa/3.0/). If you use SentiWS in
 your work, please cite the following paper:

R. Remus, U. Quasthoff & G. Heyer: SentiWS - a Publicly Available German-language Resource for Sentiment Analysis. 
In: Proceedings of the 7th International Language Ressources and Evaluation (LREC'10), 2010

"""

import warnings
warnings.filterwarnings("ignore")
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt

import re
import nltk
import unidecode
import math 
from sklearn.preprocessing import MinMaxScaler 

from nltk.corpus import opinion_lexicon
from nltk import word_tokenize 
from nltk.tokenize import treebank
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#autocorrect is not used yet cause it creates deprecation warnings that 
#for whatever aren't filtered
#from autocorrect import spell
#nltk.download('opinion_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

stemmer = PorterStemmer()

#read bag of words for positve and negative sentiment
#process data to fit our articles 
#remove document specifics, umlaute and numbers
with open("SentiWS_v1.8c_Negative.txt", "r", encoding='utf-8') as sem1:
    negative_words = sem1.read()
    negative_words = negative_words.replace('|NN', '')
    negative_words = negative_words.lower()
    negative_words = unidecode.unidecode(negative_words)
    negative_words = re.sub('[^A-Za-z]', ' ', negative_words)
sem1.close()

with open("SentiWS_v1.8c_Positive.txt", "r", encoding='utf-8') as sem2:
    positive_words = sem2.read()
    positive_words = positive_words.replace('|NN', '')
    positive_words = positive_words.lower()
    positive_words = unidecode.unidecode(positive_words)
    positive_words = re.sub('[^A-Za-z]', ' ', positive_words)
sem2.close()

positive_words = positive_words.split(',')
negative_words = negative_words.split(',')

#read the excel data 
#df = pd.read_excel("Muschg_all_2021.xlsx", index_col=0, dtype=str)
list_of_names = ['Berg', 'Buono', 'Mäder', 'Huerlimann', 'Meckel', 'Gentinetta']
dataframes_list = []
for i in range(len(list_of_names)):
    temp_df = pd.read_excel("./Train/"+list_of_names[i]+"_all_2021.xlsx", index_col=0, dtype=str)
    dataframes_list.append(temp_df)
    
#Preprocessing 
def process_summary(df):
    data = []
    for i in range(df.shape[0]):
        text = df.iloc[i, 5]

    # remove non alphabatic characters
        text = unidecode.unidecode(str(text))
        text = re.sub('[^A-Za-z]', ' ', str(text))

    # make words lowercase
        text = text.lower()

    # tokenising
        tokenized_text = word_tokenize(text)
    
    # remove stop words and no stemming yet 
        text_processed = []
        for word in tokenized_text:
            if word not in set(stopwords.words('german')):
            #here you could include the Stemmer like stemmer.stem(word) 
            #though I'm not sure if the comparison dictionary for the words also
            #includes stems, so I use the original words for now 
                text_processed.append(word)

        new_text = " ".join(text_processed)
        data.append(new_text)
    df['Processed_summary'] = data
 
def simple_sentiment(text):
    pos_words = 0
    neg_words = 0

    tokens = [word.lower() for word in word_tokenize(text)]
#    x = list(range(len(tokens))) # x axis for the plot
#    y = []
    
    for word in tokens:
        #if word in opinion_lexicon.positive():
          if word in positive_words[0]:
            pos_words += 1
#            y.append(1) # positive
        # elif word in opinion_lexicon.negative():
          if word in negative_words[0]:
            neg_words += 1
#            y.append(-1) # negative
#        else:
#            y.append(0) # neutral
# I'm not a big fan of just adding up the negative and positive words and 
# afterwards comparing the amount. If there are 6 neg words and 5 pos words, is the 
# text still positive? For now this is fine though
# we could also add numerical values here instead of words if it's better for later 
#analysis  
    if pos_words > neg_words:
        return 'Positiv'
    elif pos_words < neg_words:
        return 'Negativ'
    elif pos_words == neg_words:
        return 'Neutral'

def add_polarity(df): 
    sentiment = []
    for i in range(df.shape[0]):
        proc_sum = df.iloc[i, 7]
    
        if proc_sum == 'nan': 
            pol = 'nan'
        else:
            pol = simple_sentiment(proc_sum)
        sentiment.append(pol)
    
    df['sentiment'] = sentiment

i = 0
#calls the different functions and produces a plot for the polarity count of the article count for the author 
for dataset in dataframes_list:   
    process_summary(dataset)
    simple_sentiment(str(dataset['Processed_summary']))
    add_polarity(dataset)
    sns.countplot(dataset.sentiment)
    plt.xlabel('summary sentiment')
    plt.savefig('polarity_'+ list_of_names[i] +'.png')
    plt.clf()
    i = i + 1

def add_weight(df): 
    w = 0
    weight = []
    for i in range(df.shape[0]):
        flag = int(df.iloc[i, 6])
        summary = (df.iloc[i, 7])
        if summary == 'nan': 
            w = 0; 
        elif summary != 'nan': 
            if flag == 0: 
                w = 2;
            elif flag == 1:
                w = 1; 
            elif flag == 2:
                w = 0.5;  
        #return w;
        weight.append(w)
    df['weight'] = weight
    

sentiment_index = []   
def author_sentiment(df):
    mean = 0; 
    var = 0; 
    index_value = 0
    negative_value = 0; 
    positive_value = 0;
    neutral_value = 0;
    
    for i in range(df.shape[0]):
        sentiment = df.iloc[i, 8]
        weight = df.iloc[i, 9]
        if sentiment == 'Neutral':
                neutral_value += weight
        if sentiment == 'Positiv':
                positive_value += weight
        if sentiment == 'Negativ':
                negative_value += weight
    
    mean = (negative_value*1+neutral_value*2+positive_value*3)/(negative_value+positive_value+neutral_value)
    print(mean)
    if negative_value == max(negative_value, positive_value, neutral_value):
        var = (1-mean)**2*negative_value+(2-mean)**2*neutral_value+(3-mean)**2*positive_value
        std_var = math.sqrt(var)
        index_value = mean - (std_var/10); 
        sentiment_index.append(index_value)
    if positive_value == max(negative_value, positive_value, neutral_value):
        var = (1-mean)**2*negative_value+(2-mean)**2*neutral_value+(3-mean)**2*positive_value
        std_var = math.sqrt(var)
        index_value = mean + (std_var/10); 
        sentiment_index.append(index_value)
    if neutral_value == max(negative_value, positive_value, neutral_value):
        index_value = mean; 
        sentiment_index.append(index_value)

for dataset in dataframes_list:
   add_weight(dataset)
   author_sentiment(dataset)

print(sentiment_index)

#instead of using min, max maybe check all data at the end again, and just divide by 3 or 4 
#normalize values for the overall author sentiment
sentiment_index=[(float(i)-min(sentiment_index))/(max(sentiment_index)-min(sentiment_index)) for i in sentiment_index]

zip_sentiment = zip(list_of_names, sentiment_index)
sentiment_listing = dict(zip_sentiment)
    
print(sentiment_listing)


#concate the produced dfs to a training dataset 
all_train_dfs = pd.concat(dataframes_list)
all_train_dfs.to_excel("authors_train.xlsx")

#read 2 datasets as testdata and prepare them 
list_of_names_test = ['Bleisch', 'Rost']
dataframes_list_test = []
for i in range(len(list_of_names_test)):
    temp_df = pd.read_excel("./Test/"+list_of_names_test[i]+"_all_2021.xlsx", index_col=0, dtype=str)
    dataframes_list_test.append(temp_df)

#calls the different functions for the testdata 
for dataset in dataframes_list_test:   
    process_summary(dataset)
    simple_sentiment(str(dataset['Processed_summary']))
    add_polarity(dataset)
    add_weight(dataset)
#    author_sentiment(dataset)

#save test data as xlsx
all_test_dfs = pd.concat(dataframes_list_test)
all_test_dfs.to_excel("authors_test.xlsx")

























        