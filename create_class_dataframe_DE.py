# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 18:56:28 2021

@author: Johanna
"""

import pandas as pd
import numpy as np
from Twitter_final import get_twitter_original_DE
from Wikipedia import get_wikipedia_DE

data = pd.read_excel('Thoughtleader List_GermanSpeaking.xlsx')
data.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)
data.Twitter = data.Twitter.str.replace("@", "")
data = data.rename(columns={'Twitter' : 'id'})

# get original twitter data and add the verified part just in case for now 
twitter_data = get_twitter_original_DE()
twitter_data = twitter_data.drop(columns=['name'])

conditions = [
    (data['Twitter Verifiziert?'] == 'nicht verifiziert') | (data['Twitter Verifiziert?'] == 0),
    (data['Twitter Verifiziert?'] == 'ja')]

values = [0, 1]

data['verified'] = np.select(conditions, values)

# Get Sentiment Score of Google News
df_sentiment = pd.read_csv('Sentiment_Index_DE.csv', sep=';')
df_sentiment.rename(columns={'Index': 'Sentiment_score'}, inplace=True)

# get wikipedia
wikipedia_data = get_wikipedia_DE()

# get thoughtleader score 
#thoughtleader_score = pd.read_csv('Thoughtleaders_final.csv')

# Merge all dataframes
class_data_DE = pd.merge(data, twitter_data, on='id', how='left')
class_data_DE = pd.merge(class_data_DE, wikipedia_data, on='Name', how='left')
#class_data_DE = pd.merge(class_data_DE, thoughtleader_score, on='Name', how='left')
class_data_DE = pd.merge(class_data_DE, df_sentiment[['Name', 'Sentiment_score']], on='Name', how='left')
class_data_DE.fillna(0, inplace=True)

# drop columns that we don't need 
# class_data = class_data.drop(columns=['Unnamed: 7'])


def get_Test_DE():
    global classification_data_DE; 
    classification_data_DE = pd.DataFrame(class_data_DE)
    return classification_data_DE;