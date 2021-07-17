# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 12:18:35 2021

@author: vikto

create final dataframe with all attributes needed for classification
"""

import pandas as pd
from Twitter_final import get_twitter_factor_SW
from Twitter_final import get_twitter_factor_DE
from Wikipedia import get_wikipedia_score_SW
from Wikipedia import get_wikipedia_score_DE

#get data of .xlsx, .csv files and from other scripts
tl_SW = pd.read_excel('COINs Intelektuellen-Ranking.xlsx')
tl_DE = pd.read_excel('Thoughtleader List_GermanSpeaking.xlsx')
twitter_DE = get_twitter_factor_DE()
twitter_SW = get_twitter_factor_SW()
wikipedia_score_DE = get_wikipedia_score_DE()
wikipedia_score_DE = wikipedia_score_DE.fillna(0)
wikipedia_score_SW = get_wikipedia_score_SW()
wikipedia_score_SW = wikipedia_score_SW.fillna(0)
sentiment_DE = pd.read_csv('Sentiment_Index_DE.csv', sep=';')
sentiment_SW = pd.read_csv('Sentiment_Index.csv',  sep=';')

def prepare_data(df_gsr, wikipedia_score, twitter_score, sentiment_score):
    
    #get Google Search Result
    df_gsr.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)
    
    #Normalization of Google Search Results with min-max normalization
    df_gsr['GSR_score']=(df_gsr['GSR']-df_gsr['GSR'].min())/(df_gsr['GSR'].max()-df_gsr['GSR'].min())
    
    
    #Get Wikipedia Score
    df_wikipedia = wikipedia_score
    
    #Get Sentiment Score of Google News
    df_sentiment = sentiment_score
    df_sentiment.rename(columns={'Index': 'Sentiment_score'}, inplace=True)
    
    
    #Get Twitter Score
    df_twitter = twitter_score
    #pd.read_csv('Thoughtleader_Twitter.csv')
    df_twitter.rename(columns={'Twitter': 'Twitter_score'}, inplace=True)
    
    
    #Merge all dataframes
    df_thoughtleaders = pd.merge(df_gsr[['Name', 'GSR_score']], df_wikipedia[['Name', 'Wikipedia_score']], on='Name', how='left')
    df_thoughtleaders = pd.merge(df_thoughtleaders, df_sentiment[['Name', 'Sentiment_score']], on='Name', how='left')
    df_thoughtleaders = pd.merge(df_thoughtleaders, df_twitter[['Name', 'Twitter_score']], on='Name', how='left')
    df_thoughtleaders.fillna(0, inplace=True)

    #Calculate overall Thoughtleader Score
    df_thoughtleaders['Thoughtleader_Score']=(df_thoughtleaders['GSR_score']+df_thoughtleaders['Wikipedia_score']+df_thoughtleaders['Sentiment_score']+df_thoughtleaders['Twitter_score'])/4
   
    return df_thoughtleaders
    

Thoughtleaders_DE = prepare_data(tl_DE, wikipedia_score_DE,  twitter_DE, sentiment_DE);
Thoughtleaders_SW = prepare_data(tl_SW, wikipedia_score_SW,  twitter_SW, sentiment_SW);

def get_thoughtleaders_DE():
    global df_thoughtleaders_de; 
    df_thoughtleaders_de = pd.DataFrame(Thoughtleaders_DE)
    df_thoughtleaders_de = df_thoughtleaders_de.drop_duplicates(subset=['Name'], inplace=True)
    #df_thoughtleaders_de.to_csv('Thoughtleaders_DE_final.csv', index=False)
    return df_thoughtleaders_de;
    
def get_thoughtleaders_SW():
    global df_thoughtleaders_sw; 
    df_thoughtleaders_sw = pd.DataFrame(Thoughtleaders_SW)
    df_thoughtleaders_sw = df_thoughtleaders_sw.drop_duplicates(subset=['Name'], inplace=True)
   # df_thoughtleaders_sw = df_thoughtleaders_sw.to_csv('Thoughtleaders_SW_final.csv', index=False)
    return df_thoughtleaders_sw;

get_thoughtleaders_DE()
get_thoughtleaders_SW()



