# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 18:53:11 2021

@author: Johanna
"""

import pandas as pd
import numpy as np 
import glob

twitter_list = []

path = r'./Nodes' # use your path
all_files = glob.glob(path + "/*.parquet")

for filename in all_files:
    df = pd.read_parquet(filename, engine='pyarrow')
    twitter_list.append(df)
    
#twitter = pd.read_parquet('nodes_1.parquet', engine='pyarrow')
twitter = pd.concat(twitter_list)

#for col in twitter.columns:
#    print(col)

# absolute values: followers
# six honest signals based on chosen values: check if correct values were chosen from the data 
# central leadership: degree centrality, betweenness centrality
# rotation leadership: betweenness centrality oscillation
# balanced contribution: contribution index
# rapid response: ego art, ego nudges, alter art, alter nudges
# honest language: avg. sentiment, avg. emotionality
# shared context: avg. complexity 


twitter = twitter[['name', 'followers_count', 'degree', 'betweenness', 'betweenness_oscillation', 'contribution_index', 
                   'ego_art', 'ego_nudges', 'alter_art', 'alter_nudges', 'sentiment_avg', 'emotionality_avg',
                   'complexity_avg']]



twitter = twitter.fillna(0)

# load the thoughtleader list 
# I replaced - in the twitter account column in the thoughtleader list by nothing, so I have an nan value 

tl = pd.read_excel('Thoughtleader_List.xlsx', index_col=0, dtype=str)

tl = tl.fillna(0)

# could be possible that you need to reset the index here first
# tl = tl.reset_index()


# merge the datasets
#  already noticed there are duplicates, so check what values are correct and what can be deleted 
# also pretty sure these are not all users with twitter, so probably gotta check manually how
# names have to be changed 
twitter = twitter.rename(columns={'name' : 'Name'})
combined = pd.merge(twitter, tl, on='Name')

combined = combined.drop(columns=['Anmerkungen', 'Beruf', 'Wikipedia', 'Google Search im letzten Jahr', 'Twitter'])

conditions = [
    (combined['Twitter Verifiziert?'] == 'nicht verifiziert') | (combined['Twitter Verifiziert?'] == 0),
    (combined['Twitter Verifiziert?'] == 'verifiziert')]

values = [0, 1]

combined['verified'] = np.select(conditions, values)

# calculations for the values we need 
# followers count not added yet 
# change calculations for the honest signals if you have better idea 
combined['central_leadership'] = combined['degree'] + combined['betweenness']
combined['rotation_leadership'] = combined['betweenness_oscillation']
combined['balanced_contribution'] = combined['contribution_index']
combined['rapid_responses'] = combined['ego_art'] + combined['ego_nudges'] + combined['alter_nudges'] + combined['alter_art']
combined['honest_language'] = combined['sentiment_avg'] + combined['emotionality_avg']
combined['shared_context'] = combined['complexity_avg']


# how to calculate the end-factor?
# normalize data and then add everything up?




