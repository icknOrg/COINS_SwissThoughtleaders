# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 12:18:35 2021

@author: vikto

create final dataframe with Thoughtleader score for both the German and the Swiss people
"""

import pandas as pd
from Twitter_final import get_twitter_factor_SW
from Twitter_final import get_twitter_factor_DE
from Wikipedia import get_wikipedia_score_SW
from Wikipedia import get_wikipedia_score_DE

#get data of .xlsx, .csv files and from other scripts
tl_SW = pd.read_excel(r'CSV Data/COINs Intelektuellen-Ranking.xlsx')
tl_DE = pd.read_excel(r'CSV Data/Thoughtleader List_GermanSpeaking.xlsx')
twitter_score_DE = get_twitter_factor_DE()
twitter_score_SW = get_twitter_factor_SW()
wikipedia_score_DE = get_wikipedia_score_DE()
wikipedia_score_DE = wikipedia_score_DE.fillna(0)
wikipedia_score_SW = get_wikipedia_score_SW()
wikipedia_score_SW = wikipedia_score_SW.fillna(0)
sentiment_DE = pd.read_csv(r'CSV Data/Sentiment_Index_DE.csv', sep=';')
sentiment_SW = pd.read_csv(r'CSV Data/Sentiment_Index.csv',  sep=';')

tl = pd.concat([tl_SW, tl_DE])
twitter = pd.concat([twitter_score_SW, twitter_score_DE])
wikipedia_score = pd.concat([wikipedia_score_DE, wikipedia_score_SW])
sentiment = pd.concat([sentiment_DE, sentiment_SW])

#Normalization of twitter and wikipedia
wikipedia_score['Wikipedia_score']=(wikipedia_score['Wikipedia_score']-wikipedia_score['Wikipedia_score'].min())/(wikipedia_score['Wikipedia_score'].max()-wikipedia_score['Wikipedia_score'].min())
twitter['Twitter']=(twitter['Twitter']-twitter['Twitter'].min())/(twitter['Twitter'].max()-twitter['Twitter'].min())

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
    


def get_thoughtleader_score():
    global df_thoughtleaders; 
    Thoughtleaders = prepare_data(tl, wikipedia_score, twitter, sentiment);
    df_thoughtleaders = pd.DataFrame(Thoughtleaders)
    df_thoughtleaders.drop_duplicates(subset=['Name'], inplace=True)
    #df_thoughtleaders.to_csv(r'CSV Data/Thoughtleaders_Score_all.csv', index=False)
    return df_thoughtleaders;

#test = get_thoughtleader_score()




