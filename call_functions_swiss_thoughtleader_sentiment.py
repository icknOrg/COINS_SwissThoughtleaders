# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 20:18:32 2021

@author: Johanna
"""
"""
calls the functions from the add_sentiment file
"""

from add_sentiment import df_prep
from add_sentiment import get_list
from add_sentiment import add_weight
from add_sentiment import prepare_columns
from add_sentiment import process_summary
from add_sentiment import bert_sentiment
from add_sentiment import author_sentiment
from add_sentiment import get_listing
from add_sentiment import simple_sentiment
from add_sentiment import add_polarity
from add_sentiment import get_index 
from add_sentiment import get_df_sentiment_index

import pandas as pd
path = r'C:\Users\Johanna\Documents\GitHub\COINS_SwissTribeleaders\all'

list_of_names  = df_prep(path)
dataframes_list = get_list(list_of_names, path)
add_weight(dataframes_list, list_of_names)

prepare_columns(dataframes_list)

for dataset in dataframes_list:
    process_summary(dataset)
    simple_sentiment(str(dataset['Processed_summary']))
    add_polarity(dataset)

bert_sentiment(dataframes_list)

for dataset in dataframes_list:
    author_sentiment(dataset)

sentiment_index = get_index();

sentiment_listing = get_listing(sentiment_index, list_of_names)

sentiment_index_df = get_df_sentiment_index(sentiment_listing)

#save to csv
sentiment_index_df = pd.DataFrame(sentiment_listing.items(), columns=['Name', 'Index'])
sentiment_index_df.to_csv("Sentiment_Index.csv", encoding='utf-8')    
