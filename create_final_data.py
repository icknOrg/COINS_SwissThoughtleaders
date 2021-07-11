# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 12:18:35 2021

@author: vikto

create final dataframe with all attributes needed for classification
"""

import pandas as pd

#get Google Search Result
df_gsr = pd.read_excel('COINs Intelektuellen-Ranking.xlsx')
df_gsr.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)

#Normalization of Google Search Results with min-max normalization
df_gsr['GSR_score']=(df_gsr['GSR']-df_gsr['GSR'].min())/(df_gsr['GSR'].max()-df_gsr['GSR'].min())


#Get Wikipedia Score
df_wikipedia = pd.read_csv('Thoughtleader_Wikipedia.csv')


#Get Sentiment Score of Google News
df_sentiment = pd.read_csv('Sentiment_Index.csv', sep=',')
df_sentiment.rename(columns={'Index': 'Sentiment_score'}, inplace=True)
print(df_sentiment[df_sentiment['Name']=='Sibylle Berg'])

#Get Twitter Score
df_twitter = pd.read_csv('Thoughtleader_Twitter.csv')
df_twitter.rename(columns={'Twitter': 'Twitter_score'}, inplace=True)


#Merge all dataframes
df_thoughtleaders = pd.merge(df_gsr[['Name', 'GSR_score']], df_wikipedia[['Name', 'Wikipedia_score']], on='Name', how='left')
df_thoughtleaders = pd.merge(df_thoughtleaders, df_sentiment[['Name', 'Sentiment_score']], on='Name', how='left')
df_thoughtleaders = pd.merge(df_thoughtleaders, df_twitter[['Name', 'Twitter_score']], on='Name', how='left')
df_thoughtleaders.fillna(0, inplace=True)

#Calculate overall Thoughtleader Score
df_thoughtleaders['Thoughtleader_Score']=(df_thoughtleaders['GSR_score']+df_thoughtleaders['Wikipedia_score']+df_thoughtleaders['Sentiment_score']+df_thoughtleaders['Twitter_score'])/4

#Some duplicates occured because of the merge
#df_thoughtleaders.drop_duplicates(inplace=True)

print(df_thoughtleaders)
df_thoughtleaders.to_csv('Thoughtleaders_final.csv', index=False)