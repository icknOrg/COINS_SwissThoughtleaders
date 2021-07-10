# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 12:18:35 2021

@author: vikto

create final dataframe with all attributes needed for classification
"""

import pandas as pd

df_gsr = pd.read_excel('COINs Intelektuellen-Ranking.xlsx')
df_gsr.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)

df_wikipedia = pd.read_csv('Thoughtleader_Wikipedia.csv')

df_sentiment = pd.read_csv('Sentiment_Index.csv', sep=';')
df_sentiment.rename(columns={'Index': 'Sentiment_score'}, inplace=True)

#df_twitter = pd.read_csv('')

df_thoughtleaders = pd.merge(df_gsr[['Name', 'GSR']], df_wikipedia[['Name', 'Wikipedia_score']], on='Name', how='left')
df_thoughtleaders = pd.merge(df_thoughtleaders, df_sentiment, on='Name', how='left')
#df_thoughtleaders = pd.merge(df_thoughtleaders, df_twitter, on='Name', how='left')

df_thoughtleaders.to_csv('Thoughtleaders_final.csv')