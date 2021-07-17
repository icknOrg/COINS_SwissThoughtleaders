# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:14:37 2021

@author: Johanna
"""
"""
The sentiment Index is calculated by combining two different methods of assigning a sentiment to the article,
first by applying a bag of words for the German Language called SentiWS and comparing its words to the articles, 
second by using BERT implemented in a sentiment model that assigns sentiments to an article. 
A weight is applied to each article that consists of how often the persons name is mentioned in the 
description of the article (mostly ranging from 0 to 2). 

The Author's Index is then calculated by comparing the both sentiments of BERT and SentiWS and how often these values overlap 
in negative, neutral and positive articles using the weight to let the article weigh more or less 
in the calculation. 

In order to let the index deviate more into a negative/positive area (since the overall calculation showed to even out
articles in a neutral area), the mean of the values is calculated and the standard deviation divided by 10 is 
added of the max value is positive and substracted if the max value is negative. 

Afterwards the value gets normalized in a Min/Max (in a range from 0 to 1). 

The results together with the names of the persons are saved in a dataframe and returned. 

Keep in mind if you haven't used CUDA yet, you might have to assign your GPU device first. Without an error might occur.
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
import pandas as pd 
import glob
# seaborn as sns 
# import matplotlib.pyplot as plt

import re
import nltk
import unidecode
import math 
from nltk import word_tokenize 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# for bert sentiment
from germansentiment import SentimentModel
import torch

# download necessary documents for pre-processing 
nltk.download('punkt')
nltk.download('stopwords')

stemmer = PorterStemmer()

# read bag of words for positve and negative sentiment
# process data to fit our articles 
# remove document specifics, umlaute and numbers
with open("SentiWS_v2.0_Negative.txt", "r", encoding='utf-8') as sem1:
    negative_words = sem1.read()
    negative_words = negative_words.replace('|NN', '')
    negative_words = negative_words.lower()
    negative_words = unidecode.unidecode(negative_words)
    negative_words = re.sub('[^A-Za-z]', ' ', negative_words)
sem1.close()

with open("SentiWS_v2.0_Positive.txt", "r", encoding='utf-8') as sem2:
    positive_words = sem2.read()
    positive_words = positive_words.replace('|NN', '')
    positive_words = positive_words.lower()
    positive_words = unidecode.unidecode(positive_words)
    positive_words = re.sub('[^A-Za-z]', ' ', positive_words)
sem2.close()

positive_words = positive_words.split(',')
negative_words = negative_words.split(',')

# read the excel data and prepare the dataframe list
# path = r'C:\Users\Johanna\Documents\GitHub\COINS_SwissTribeleaders\all' # use your path

def df_prep(path):
    list_of_names = []
    all_files = glob.glob(path + "/*.xlsx")
    
    for filename in all_files:
        filename = filename.replace(path, "")
        filename = filename.replace(".xlsx", "")
        filename = filename.replace("\\", "")
        list_of_names.append(filename)
    return list_of_names;

def get_list(list_of_names, path):
    dataframes_list = []
    for i in range(len(list_of_names)):
        temp_df = pd.read_excel(path+"/"+list_of_names[i]+".xlsx", index_col=0, dtype=str)
        dataframes_list.append(temp_df)
    return dataframes_list;

# add the weight for the articles based on how often the name is mentioned in description
def add_weight(dataframes_list, list_of_names):
    a = 0
    for dataset in dataframes_list:
        dataset["count"]= dataset["desc"].str.count(list_of_names[a], re.I)
        a += 1

def drop_columns(df): 
    df = df.drop(columns=['title', 'media', 'date', 'desc', 'link'], axis='columns', inplace=True)

def prepare_columns(dataframes_list):
    for dataset in dataframes_list:
        drop_columns(dataset)
        
    for dataset in dataframes_list:
        if 'flag' in dataset:
            dataset = dataset.drop(columns=['flag'], axis='columns', inplace=True)
    
    for dataset in dataframes_list:
        if 'datetime' in dataset:
            dataset = dataset.drop(columns=['datetime'], axis='columns', inplace=True) 
            
    for dataset in dataframes_list:
        if 'img' in dataset:
            dataset = dataset.drop(columns=['img'], axis='columns', inplace=True)      
            
    for dataset in dataframes_list: 
        #dataset = dataset[dataset.count != 0]
        dataset.drop(dataset.loc[dataset['count']==0].index, inplace=True)
    
    for dataset in dataframes_list:
        dataset.dropna(inplace=True)
        
# Preprocessing 
def process_summary(df):
    data = []
    for i in range(df.shape[0]):
        text = df.iloc[i, 0]

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
            #though since sentiWS has all versions of a word it is not necessary 
                text_processed.append(word)

        new_text = " ".join(text_processed)
        data.append(new_text)
    df['Processed_summary'] = data

# count the positive and negative words and return the overall sentiment
def simple_sentiment(text):
    pos_words = 0
    neg_words = 0

    tokens = [word.lower() for word in word_tokenize(text)]
    
    for word in tokens:
          if word in positive_words[0]:
            pos_words += 1

          if word in negative_words[0]:
            neg_words += 1
 
    if pos_words > neg_words:
        return 'Positiv'
    elif pos_words < neg_words:
        return 'Negativ'
    elif pos_words == neg_words:
        return 'Neutral'

# add the sentiment to the dataset 
def add_polarity(df): 
    sentiment = []
    for i in range(df.shape[0]):
        proc_sum = df.iloc[i, 2]
    
        if proc_sum == 'nan': 
            pol = 'nan'
        else:
            pol = simple_sentiment(proc_sum)
        sentiment.append(pol)
    
    df['sentiment'] = sentiment

# add the bert sentiment

# you could use this to save the dataset in different partitions if its too big for one run for you
# dataframes_fifth = []
# i = 51; 
# for dataset in dataframes_list:
#     if i <= 71:
#         dataframes_fifth.append(dataset)
#         i+=1;  
#     else:
#         pass;
# in here run the sentiment model first, then the next two lines
# dataframes_fifth = pd.concat(dataframes_fifth)
# dataframes_fifth.to_csv("DF_5.csv", encoding='utf-8')

def bert_sentiment(dataframes_list): 
    model = SentimentModel()
    sentiment = []
    summaries = []
    
    for dataset in dataframes_list: 
        for i in range(dataset.shape[0]): 
            summary = dataset.iloc[i, 2]
            summaries.append(summary)
        if dataset.empty == False:
            sentiment.append(model.predict_sentiment(summaries))
        else:
            sentiment.append(0)
        dataset['sentiment_bert'] = sentiment[0]
        summaries = []
        sentiment = []
        torch.cuda.empty_cache()
        
# add sentiment index per author
sentiment_index = []
def author_sentiment(df): 
    var = 0; 
    index_value = 0
    negative_value = 0; 
    positive_value = 0;
    neutral_value = 0;
    neg_bit_value = 0; 
    pos_bit_value = 0; 

    if df.empty != True: 
        for i in range(df.shape[0]):
            sentiment = df.iloc[i, 3]
            sentiment_bert = df.iloc[i, 4]
            weight = df.iloc[i, 1]
            
            if sentiment == 'Neutral': 
                if sentiment_bert == "neutral":
                    neutral_value += weight
                elif sentiment_bert == "positive": 
                    pos_bit_value += weight 
                elif sentiment_bert == "negative":
                    neg_bit_value += weight
            elif sentiment == 'Positiv':
                if sentiment_bert == "neutral":
                    pos_bit_value += weight
                elif sentiment_bert == "positive": 
                    positive_value += weight
                elif sentiment_bert == "negative":
                    neutral_value += weight
            elif sentiment == 'Negativ':
                if sentiment_bert == "neutral":
                    neg_bit_value += weight
                elif sentiment_bert == "positive": 
                    neutral_value += weight
                elif sentiment_bert == "negative":
                    negative_value += weight
        
        if (negative_value+positive_value+neutral_value+pos_bit_value+neg_bit_value) > 0: 
            mean = (negative_value*1+neg_bit_value*2+neutral_value*3+pos_bit_value*4+positive_value*5)/(negative_value+positive_value+neutral_value+pos_bit_value+neg_bit_value)
            if negative_value == max(negative_value, neg_bit_value, positive_value, pos_bit_value, neutral_value):
                var = (1-mean)**2*negative_value+(2-mean)**2*neg_bit_value+(3-mean)**2*neutral_value+(4-mean)**2*pos_bit_value+(5-mean)**2*positive_value
                std_var = math.sqrt(var)
                index_value = mean - (std_var/10); 
                sentiment_index.append(index_value)
            elif positive_value == max(negative_value, neg_bit_value, positive_value, pos_bit_value, neutral_value):
                var = (1-mean)**2*negative_value+(2-mean)**2*neg_bit_value+(3-mean)**2*neutral_value+(4-mean)**2*pos_bit_value+(5-mean)**2*positive_value
                std_var = math.sqrt(var)
                index_value = mean + (std_var/10); 
                sentiment_index.append(index_value)
            elif neutral_value == max(negative_value, neg_bit_value, positive_value, pos_bit_value, neutral_value):
                index_value = mean; 
                sentiment_index.append(index_value)
            elif neg_bit_value == max(negative_value, neg_bit_value, positive_value, pos_bit_value, neutral_value):
                var = (1-mean)**2*negative_value+(2-mean)**2*neg_bit_value+(3-mean)**2*neutral_value+(4-mean)**2*pos_bit_value+(5-mean)**2*positive_value
                std_var = math.sqrt(var)
                index_value = mean - (std_var/50);
                sentiment_index.append(index_value)
            elif pos_bit_value == max(negative_value, neg_bit_value, positive_value, pos_bit_value, neutral_value):
                var = (1-mean)**2*negative_value+(2-mean)**2*neg_bit_value+(3-mean)**2*neutral_value+(4-mean)**2*pos_bit_value+(5-mean)**2*positive_value
                std_var = math.sqrt(var)
                index_value = mean + (std_var/50); 
                sentiment_index.append(index_value)

        else: 
            mean = 0; 
            index_value = mean
            sentiment_index.append(index_value)
    else:
        sentiment_index.append(0)

# get the index
def get_index(): 
    return sentiment_index; 

# normalize values for the overall author sentiment
def get_listing(sentiment_index, list_of_names):
    sentiment_index=[(float(i)-min(sentiment_index))/(max(sentiment_index)-min(sentiment_index)) for i in sentiment_index]
    
    zip_sentiment = zip(list_of_names, sentiment_index)
    sentiment_listing = dict(zip_sentiment)
        
    return sentiment_listing

# get the sentiment index in a df
def get_df_sentiment_index(sentiment_listing): 
     global sentiment_index_df;
     sentiment_index_df = pd.DataFrame(sentiment_listing.items(), columns=['Name', 'Index'])
     return sentiment_index_df
   



























        
