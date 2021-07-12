# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 21:54:22 2021

@author: Johanna

load the different dfs and tables with the data that we want to use for the classification 
"""

import pandas as pd
import numpy as np
from Twitter_final import get_twitter_original
from Wikipedia import get_wikipedia

data = pd.read_excel('COINs Intelektuellen-Ranking.xlsx')
data.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)
data.Twitter = data.Twitter.str.replace("@", "")
data = data.rename(columns={'Twitter' : 'id'})

# get original twitter data and add the verified part just in case for now 
twitter_data = get_twitter_original()
twitter_data = twitter_data.drop(columns=['Name'])

conditions = [
    (data['Twitter Verifiziert?'] == 'nicht verifiziert') | (data['Twitter Verifiziert?'] == 0),
    (data['Twitter Verifiziert?'] == 'verifiziert')]

values = [0, 1]

data['verified'] = np.select(conditions, values)

# Get Sentiment Score of Google News
df_sentiment = pd.read_csv('Sentiment_Index.csv', sep=';')
df_sentiment.rename(columns={'Index': 'Sentiment_score'}, inplace=True)

# get wikipedia
wikipedia_data = get_wikipedia()

# Merge all dataframes
class_data = pd.merge(data, twitter_data, on='id', how='left')
class_data = pd.merge(class_data, wikipedia_data, on='Name', how='left')
class_data = pd.merge(class_data, df_sentiment[['Name', 'Sentiment_score']], on='Name', how='left')
class_data.fillna(0, inplace=True)

# drop columns that we don't need 
class_data = class_data.drop(columns=['Unnamed: 7'])

# function to retrieve classification data in the code for the classification model
def get_class_original():
    global classification_data; 
    classification_data = pd.DataFrame(class_data)
    return classification_data;