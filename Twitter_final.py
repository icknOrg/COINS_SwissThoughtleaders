#!/usr/bin/env python
# coding: utf-8

"""
Created on Sun Jun 20 18:53:11 2021

@author: Johanna

Load the nodes data that was fetched with Griffin for the persons that have a Twitter account. 
Calculate the Twitter Index based on the columns that define the honest signals.

@ Johanna 18.07.2021:
    Added certain persona from German data for extra calculation since data was missing in Griffin Data
"""

import pandas as pd
import numpy as np 
import glob

# read nodes data
path_DE = r'Nodes_DE/Swiss German nodes.csv'
path_SW = r'Nodes_SW'

def load_nodes_data(path):
    twitter_list = []
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

def load_nodes_csv(path):
    
# get Twitter Data for German data
# since many of the important people were not incldued in the twitter data we chose some specific persons
# we calculate the mean and add the follower count 
# then proceed as usual with normalisation 

    twitter_DE = pd.read_csv(path)        
    twitter_DE.id = twitter_DE.id.str.lower()    
    twitter_DE = twitter_DE[['id', 'name', 'followers_count', 'degree', 'betweenness', 'contribution_index', 
                       'sentiment_avg', 'emotionality_avg', 'ego_art', 'ego_nudges', 'alter_art', 'alter_nudges',
                       'complexity_avg', 'betweenness_oscillation']]  
    twitter_DE = twitter_DE.fillna(0)
    
    Empties = {'janboehm': 2324793, 'Karl_Lauterbach': 556072, 'frank_thelen': 58203, 'rezomusik': 471174, 'maithi_nk': 327247, 'officiallyjoko': 2148369, 'Luisamneubauer': 263300,
                'SophiePassmann': 181300, 'SporkPeter': 1227, 'FuestClemens': 24600, 'saschalobo': 760900, 'richprecht': 3180, 'Natascha_Strobl': 125600, 'PinarAtalay': 27200,
                'Sloterdijk_P': 5917, 'Mirjam_Fischer': 14000, 'BrinkmannLab': 103700, 'MalcolmOhanwe': 30600, 'beyond_ideology': 77000, 'kathrinpassig': 34900, 'KaiDiekmann': 178400, 
                'JoyceIlg': 326000, 'EckerleIsabella': 54600, 'DenizUtlu': 2040, 'ardenthistorian': 43200, '_AliceSchwarzer': 2318}
    Empties = pd.DataFrame(Empties.items(),  columns=['id', 'followers_count'])
    Empties.id = Empties.id.str.lower()    

    degree = twitter_DE.degree.mean()
    betweenness = twitter_DE.betweenness.mean()
    contribution_index = twitter_DE.contribution_index.mean()
    sentiment_avg = twitter_DE.sentiment_avg.mean()
    emotionality_avg = twitter_DE.emotionality_avg.mean()
    ego_art = twitter_DE.ego_art.mean()
    ego_nudges = twitter_DE.ego_nudges.mean()
    alter_art = twitter_DE.alter_art.mean()
    alter_nudges = twitter_DE.alter_nudges.mean()
    complexity_avg = twitter_DE.complexity_avg.mean()
    betweenness_oscillation = twitter_DE.betweenness_oscillation.mean()

    for i in range(Empties.shape[0]): 
        Empties['degree'] = degree
        Empties['betweenness'] = betweenness
        Empties['contribution_index'] = contribution_index
        Empties['sentiment_avg'] = sentiment_avg
        Empties['emotionality_avg'] = emotionality_avg
        Empties['ego_art'] = ego_art
        Empties['ego_nudges'] = ego_nudges
        Empties['alter_art'] = alter_art
        Empties['alter_nudges'] = alter_nudges
        Empties['complexity_avg'] = complexity_avg
        Empties['betweenness_oscillation'] = betweenness_oscillation
               
    twitter_DE = twitter_DE.merge(Empties, on="id", how="left")
    twitter_DE = twitter_DE.assign(followers_count_x = twitter_DE.followers_count_y.fillna(twitter_DE.followers_count_x)).drop('followers_count_y', axis=1)
    twitter_DE = twitter_DE.assign(degree_x = twitter_DE.degree_y.fillna(twitter_DE.degree_x)).drop('degree_y', axis=1)
    twitter_DE = twitter_DE.assign(betweenness_x = twitter_DE.betweenness_y.fillna(twitter_DE.betweenness_x)).drop('betweenness_y', axis=1)
    twitter_DE = twitter_DE.assign(contribution_index_x = twitter_DE.contribution_index_y.fillna(twitter_DE.contribution_index_x)).drop('contribution_index_y', axis=1)
    twitter_DE = twitter_DE.assign(sentiment_avg_x = twitter_DE.sentiment_avg_y.fillna(twitter_DE.sentiment_avg_x)).drop('sentiment_avg_y', axis=1)
    twitter_DE = twitter_DE.assign(emotionality_avg_x = twitter_DE.emotionality_avg_y.fillna(twitter_DE.emotionality_avg_x)).drop('emotionality_avg_y', axis=1)
    twitter_DE = twitter_DE.assign(ego_art_x = twitter_DE.ego_art_y.fillna(twitter_DE.ego_art_x)).drop('ego_art_y', axis=1)
    twitter_DE = twitter_DE.assign(ego_nudges_x = twitter_DE.ego_nudges_y.fillna(twitter_DE.ego_nudges_x)).drop('ego_nudges_y', axis=1)
    twitter_DE = twitter_DE.assign(complexity_avg_x = twitter_DE.complexity_avg_y.fillna(twitter_DE.complexity_avg_x)).drop('complexity_avg_y', axis=1)
    twitter_DE = twitter_DE.assign(alter_nudges_x = twitter_DE.alter_nudges_y.fillna(twitter_DE.alter_nudges_x)).drop('alter_nudges_y', axis=1)
    twitter_DE = twitter_DE.assign(alter_art_x = twitter_DE.alter_art_y.fillna(twitter_DE.alter_art_x)).drop('alter_art_y', axis=1)
    twitter_DE = twitter_DE.assign(betweenness_oscillation_x = twitter_DE.betweenness_oscillation_y.fillna(twitter_DE.betweenness_oscillation_x)).drop('betweenness_oscillation_y', axis=1)

    twitter_DE = twitter_DE.rename(columns={'followers_count_x' : 'followers_count'})
    twitter_DE = twitter_DE.rename(columns={'degree_x' : 'degree'})
    twitter_DE = twitter_DE.rename(columns={'betweenness_x' : 'betweenness'})
    twitter_DE = twitter_DE.rename(columns={'contribution_index_x' : 'contribution_index'})
    twitter_DE = twitter_DE.rename(columns={'sentiment_avg_x' : 'sentiment_avg'})
    twitter_DE = twitter_DE.rename(columns={'emotionality_avg_x' : 'emotionality_avg'})
    twitter_DE = twitter_DE.rename(columns={'ego_art_x' : 'ego_art'})
    twitter_DE = twitter_DE.rename(columns={'ego_nudges_x' : 'ego_nudges'})
    twitter_DE = twitter_DE.rename(columns={'alter_art_x' : 'alter_art'})
    twitter_DE = twitter_DE.rename(columns={'alter_nudges_x' : 'alter_nudges'})
    twitter_DE = twitter_DE.rename(columns={'complexity_avg_x' : 'complexity_avg'})
    twitter_DE = twitter_DE.rename(columns={'betweenness_oscillation_x' : 'betweenness_oscillation'})

    return twitter_DE;


# absolute values: followers
# six honest signals based on chosen values: check if correct values were chosen from the data 
# central leadership: degree centrality, betweenness centrality
# rotation leadership: betweenness centrality oscillation
# balanced contribution: contribution index
# rapid response: ego art, ego nudges, alter art, alter nudges
# honest language: avg. sentiment, avg. emotionality
# shared context: avg. complexity 


rank_SW = r'CSV Data/COINs Intelektuellen-Ranking.xlsx'
rank_DE = r'CSV Data/Thoughtleader List_GermanSpeaking.xlsx'

def prepare_data(path):
    data = pd.read_excel(path)
    data.rename(columns={'Google Search Results (this year)': 'GSR'}, inplace=True)
    data.Twitter = data.Twitter.str.replace("@", "")
    data.Twitter = data.Twitter.str.lower()
    data = data.rename(columns={'Twitter' : 'id'})
    return data;

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
    combined['Twitter'] = combined['central_leadership'] + combined['rotation_leadership'] + combined['balanced_contribution'] + combined['rapid_responses'] + combined['honest_language'] + combined['shared_context']+(combined['followers_count']/100)
    
    #drop unncessary columns 
    combined = combined[['Name', 'Twitter']]

    return combined;

# call functions
nodes_DE = load_nodes_data(path_SW);
nodes_SW = load_nodes_data(path_SW);

data_DE = prepare_data(rank_DE);
data_SW = prepare_data(rank_SW);

#twitter_DE = create_final_twitter(nodes_DE, data_DE)
#twitter_SW = create_final_twitter(nodes_SW, data_SW)


def get_twitter_original_DE():
    global twitter_original_DE;
    nodes_DE = load_nodes_csv(path_SW);
    twitter_original_DE = pd.DataFrame(nodes_DE)
    return twitter_original_DE;

def get_twitter_original_SW():
    global twitter_original_SW; 
    nodes_SW = load_nodes_data(path_SW);
    twitter_original_SW = pd.DataFrame(nodes_SW)
    return twitter_original_SW;

def get_twitter_factor_SW(): 
    global twitter_factor_SW; 
    twitter_SW = create_final_twitter(nodes_SW, data_SW)
    twitter_factor_SW = pd.DataFrame(twitter_SW)
    twitter_factor_SW.replace([np.inf, -np.inf], np.nan, inplace=True)
    twitter_factor_SW = twitter_factor_SW.fillna(0)
    twitter_factor_SW['Twitter']=(twitter_factor_SW['Twitter']-twitter_factor_SW['Twitter'].min())/(twitter_factor_SW['Twitter'].max()-twitter_factor_SW['Twitter'].min())
    return twitter_factor_SW;

def get_twitter_factor_DE(): 
   global twitter_factor_DE; 
   twitter_DE = create_final_twitter(nodes_DE, data_DE)
   twitter_factor_DE = pd.DataFrame(twitter_DE)
   twitter_factor_DE.replace([np.inf, -np.inf], np.nan, inplace=True)
   twitter_factor_DE = twitter_factor_DE.fillna(0)
   twitter_factor_DE['Twitter']=(twitter_factor_DE['Twitter']-twitter_factor_DE['Twitter'].min())/(twitter_factor_DE['Twitter'].max()-twitter_factor_DE['Twitter'].min())
   return twitter_factor_DE;



