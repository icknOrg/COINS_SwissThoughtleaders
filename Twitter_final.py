#!/usr/bin/env python
# coding: utf-8

"""
Created on Sun Jun 20 18:53:11 2021

@author: Johanna

Load the nodes data that was fetched with Griffin for the persons that have a Twitter account. 
Calculate the Twitter Index based on the columns that define the honest signals.
"""

import pandas as pd
import numpy as np 
import glob

twitter_list = []

# read nodes data
path = r'./Nodes_DE' # use your path
path2 = r'Nodes_SW'

def load_nodes_data(path):
    all_files = glob.glob(path + "/*.parquet")
    
    for filename in all_files:
        df = pd.read_parquet(filename, engine='pyarrow')
        twitter_list.append(df)
        
    twitter = pd.concat(twitter_list)
    twitter.id = twitter.id.str.lower()
    
    twitter = twitter[['id', 'name', 'followers_count', 'degree', 'betweenness', 'contribution_index', 
                       'sentiment_avg', 'emotionality_avg', 'ego_art', 'ego_nudges', 'alter_art', 'alter_nudges',
                       'complexity_avg', 'betweenness_oscillation']]
    
    twitter = twitter.fillna(0)
    
    return twitter;
# absolute values: followers
# six honest signals based on chosen values: check if correct values were chosen from the data 
# central leadership: degree centrality, betweenness centrality
# rotation leadership: betweenness centrality oscillation
# balanced contribution: contribution index
# rapid response: ego art, ego nudges, alter art, alter nudges
# honest language: avg. sentiment, avg. emotionality
# shared context: avg. complexity 


rank_SW = 'COINs Intelektuellen-Ranking.xlsx'
rank_DE = 'Thoughtleader List_GermanSpeaking.xlsx'

def prepare_data(path):
    data = pd.read_excel(path)
    data.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)
    data.Twitter = data.Twitter.str.replace("@", "")
    data.Twitter = data.Twitter.str.lower()
    data = data.rename(columns={'Twitter' : 'id'})
    return data;
    #df = xls.parse(parse_cols=[0, 1, 2, 3], index_col=0, nrows=100, usecols = "A,B,C,D,E,F,G", na_values=[0])
    
    #print(df["Twitter_id"].value_counts())

def create_final_twitter(twitter, data):
    combined = pd.merge(twitter, data, on='id')
    
    conditions = [
        (combined['Twitter Verifiziert?'] == 'nicht verifiziert') | (combined['Twitter Verifiziert?'] == 0),
        (combined['Twitter Verifiziert?'] == 'ja')]
    
    values = [0, 1]
    
    combined['verified'] = np.select(conditions, values)
    
    combined = combined.drop(columns=['Bereich', 'Wikipedia', 'GSR', 'Twitter Verifiziert?', 'm/w'])
    
    # calculations for the values we need 
    combined['central_leadership'] = combined['degree'] + combined['betweenness']
    combined['rotation_leadership'] = combined['betweenness_oscillation']
    combined['balanced_contribution'] = combined['contribution_index']
    combined['rapid_responses'] = (1/combined['ego_art']) + (1/combined['ego_nudges']) + (1/combined['alter_nudges']) + (1/combined['alter_art'])
    combined['honest_language'] = combined['sentiment_avg'] + combined['emotionality_avg']
    combined['shared_context'] = combined['complexity_avg']
    #combined = combined.fillna(0)
    combined['Twitter'] = combined['central_leadership'] + combined['balanced_contribution'] + (1/combined['rapid_responses']) + combined['honest_language'] + combined['shared_context']+(combined['followers_count']/100)
    
    #drop unncessary columns 
    combined = combined[['Name', 'Twitter']]
    #print(combined)
    #Merge with tl again, to get the original name of the thoughtleader and not the name of the wikipedia page
    #final_twitter = pd.merge(data, combined, on='Name', how="left")
    
    #final_twitter.drop(columns=['Bereich', 'Wikipedia', 'GSR', "Twitter Verifiziert?", "m/w"], inplace=True)
    return combined;

#final_twitter.to_csv("Thoughtleader_Twitter.csv", encoding='utf-8')

# call functions
nodes_DE = load_nodes_data(path);
nodes_SW = load_nodes_data(path2);

data_DE = prepare_data(rank_DE);
data_SW = prepare_data(rank_SW);

twitter_DE = create_final_twitter(nodes_DE, data_DE)
twitter_SW = create_final_twitter(nodes_SW, data_SW)


def get_twitter_original_DE():
    global twitter_original_DE; 
    twitter_original_DE = pd.DataFrame(nodes_DE)
    return twitter_original_DE;

def get_twitter_original_SW():
    global twitter_original_SW; 
    twitter_original_SW = pd.DataFrame(nodes_SW)
    return twitter_original_SW;

def get_twitter_factor_SW(): 
    global twitter_factor_SW; 
    twitter_factor_SW = pd.DataFrame(twitter_SW)    
    twitter_factor_SW['Twitter']=(twitter_factor_SW['Twitter']-twitter_factor_SW['Twitter'].min())/(twitter_factor_SW['Twitter'].max()-twitter_factor_SW['Twitter'].min())
    return twitter_factor_SW;

def get_twitter_factor_DE(): 
    global twitter_factor_DE; 
    twitter_factor_DE = pd.DataFrame(twitter_DE)    
    twitter_factor_DE['Twitter']=(twitter_factor_DE['Twitter']-twitter_factor_DE['Twitter'].min())/(twitter_factor_DE['Twitter'].max()-twitter_factor_DE['Twitter'].min())
    return twitter_factor_DE;

