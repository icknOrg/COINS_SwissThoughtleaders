# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:50:02 2021

@author: Johanna
Part for fetching Google News data on some potential Swiss Thoughtleaders
Beware: using loops or too many runs in a row will cause an Error 429: Too many Requests
This Error couldn't be overgone by using a VPN 
After that  the IP Address is blocked for a certain time by Google and requires you to wait
Also max of results in one run are 10 articles -> hence the procedure:
    One run is for half a month, after that combined the data rows in Excel manually
    - time consuming but better than desperately searching for a work around that might 
    not work in the end anyway!
Prodecure: 
    Searching for the author and fetching data twice a month, from beginning to middle, 
    from middle to end of month in 2021. Last month: 01.05. to 10.05. 
@author: Viktoria
Added the try except as downloading of articles sometime did not work 
which resulted in not getting any articles for the specific time period
"""

   
from GoogleNews import GoogleNews
import pandas as pd
from newspaper import Article
from newspaper import Config

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

googlenews = GoogleNews(lang='de', start='03/01/2021', end='03/14/2021', encode='utf-8')
googlenews.search('Zora del Buono')
result=googlenews.result()
df=pd.DataFrame(result)

dict={}
for ind in df.index:
    article = Article(df['link'][ind],config=config)
    
    try:
        article.download()
        article.parse()
        article.nlp()
        dict[ind]=article.summary
    except:
        print('***FAILED TO DOWNLOAD***', article.url)
        continue
    
df['summary'] = df.index.map(dict)
df.to_excel("articles_Buono_Mar_1.xlsx")


















