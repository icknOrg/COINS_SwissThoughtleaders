# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 21:54:22 2021

@author: vikto

load the different dfs and tables with the data that we want to use for the classification
and calculate the classification labels based on the Thoughtleader scores of the dataframe 
with both the German and the Swiss people  
"""

import pandas as pd
import numpy as np

from Twitter_final import get_twitter_original_SW
from Twitter_final import get_twitter_original_DE
from Wikipedia import get_wikipedia_SW
from Wikipedia import get_wikipedia_DE
from thoughtleader_index_all import get_thoughtleader_score


tl_SW = pd.read_excel(r'CSV Data/COINs Intelektuellen-Ranking.xlsx')
tl_DE = pd.read_excel(r'CSV Data/Thoughtleader List_GermanSpeaking.xlsx')
twitter_DE = get_twitter_original_DE()
twitter_SW = get_twitter_original_SW()
wikipedia_DE = get_wikipedia_DE()
wikipedia_SW = get_wikipedia_SW()
score = get_thoughtleader_score()

x = score[['Thoughtleader_Score']].sort_values(by='Thoughtleader_Score',ascending=False)[(score[['Thoughtleader_Score']].sort_values(by='Thoughtleader_Score',ascending=False).cumsum()
  
                                                                                          /score[['Thoughtleader_Score']].sort_values(by='Thoughtleader_Score',ascending=False).sum())<=.5].dropna()
# add labels
class_labels = []
for value in score.index: 
    if value in x.index:
        class_labels.append(1)
    else:
        class_labels.append(0)
    
score['class_labels'] = class_labels

def prepare_data(data, wikipedia, twitter, score):
    
    data.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)
    data.Twitter = data.Twitter.str.replace("@", "")
    data = data.rename(columns={'Twitter' : 'id'})
    
    # get original twitter data and add the verified part just in case for now 
    twitter_data = twitter
    twitter_data = twitter_data.drop(columns=['name'])
    
    conditions = [
        (data['Twitter Verifiziert?'] == 'nicht verifiziert') | (data['Twitter Verifiziert?'] == 0),
        (data['Twitter Verifiziert?'] == 'ja')]
    
    values = [0, 1]
    
    data['verified'] = np.select(conditions, values)
    
    # Get Sentiment Score of Google News
    #df_sentiment = pd.read_csv('Sentiment_Index.csv', sep=';')
    #df_sentiment.rename(columns={'Index': 'Sentiment_score'}, inplace=True)
    
    # get wikipedia
    wikipedia_data = wikipedia
    
    # get thoughtleader score
    thoughtleader_score = score
    
    # Merge all dataframes
    class_data = pd.merge(data, twitter_data, on='id', how='left')
    class_data = pd.merge(class_data, wikipedia_data, on='Name', how='left')
    class_data = pd.merge(class_data, thoughtleader_score, on='Name', how='left')
    #class_data = pd.merge(class_data, df_sentiment[['Name', 'Sentiment_score']], on='Name', how='left')
    class_data.fillna(0, inplace=True)
    class_data.drop_duplicates(subset=['Name'], inplace=True)

    return class_data

Classification_DE = prepare_data(tl_DE, wikipedia_DE, twitter_DE, score);
Classification_SW = prepare_data(tl_SW,  wikipedia_SW, twitter_SW, score);

# function to retrieve classification data in the code for the classification model
def get_class_original_DE():
    global classification_data_de; 
    classification_data_de = pd.DataFrame(Classification_DE)
    classification_data_de.to_csv(r'CSV Data/Classified_Thoughtleaders_DE_from_all.csv')
    return classification_data_de;

def get_class_original_SW():
    global classification_data_sw; 
    classification_data_sw = pd.DataFrame(Classification_SW)
    classification_data_sw.to_csv(r'CSV Data/Classified_Thoughtleaders_SW_from_all.csv')
    return classification_data_sw;

