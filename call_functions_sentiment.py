# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 20:18:32 2021

@author: Johanna
"""
"""
calls the functions from the add_sentiment file
"""

from sentiment_analysis import df_prep
from sentiment_analysis import get_list
from sentiment_analysis import add_weight
from sentiment_analysis import prepare_columns
from sentiment_analysis import process_summary
from sentiment_analysis import bert_sentiment
from sentiment_analysis import author_sentiment
from sentiment_analysis import get_listing
from sentiment_analysis import simple_sentiment
from sentiment_analysis import add_polarity
from sentiment_analysis import get_index 
from sentiment_analysis import get_df_sentiment_index

import pandas as pd
path = r'all_SW_Articles'

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
sentiment_index_df.to_csv(r'CSV Data/Sentiment_Index.csv', encoding='utf-8')    
