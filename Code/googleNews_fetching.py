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
    
@author: Viktoria
Added the try except as downloading of articles sometime did not work 
which resulted in not getting any articles for the specific time period
"""

# authors = ['Lukas Bärfuss', 'Jonas Lüscher', 'Charles Lewinski', 'Adolf Muschg', 
#            'Ludwig Hasler', 'Martin Meyer', 'Ueli Mäder', 'Martin R. Dean', 
#            'Peter Bichsel', 'Jürg Halter', 'Rolf Dobelli', 'Thomas Hürlimann','Milena Moser', 
#            'Barbara Bleisch', 'Annemarie Piper', 'Sibylle Berg', 'Katja Rost', 
#            'Zora del Buono', 'Katja Gentinetta', 'Miriam Meckel']
   
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

"""
Created on Tue May 11 15:50:02 2021

@author: Johanna
The following part is for coverting any XLSX to JSON  
keep in mind that this version directly coverts the data to a json file
the file has to be renamed in the folder accordingly afterwards
"""
# excelFilePath = 'C:/Users/Johanna/.spyder-py3/Authors/Lukas Bärfuss/Bärfuss_all_2021.xlsx'
# import excel2json
# excel2json.convert_from_file(excelFilePath)

"""
TO DO
- check data for correctness: 
    - check if the articles are actually for the authors cause I noticed that some aren't for the authors e.g. Hasler and Meyer 
    - some empty values for summary since no data available apparently
    - check for duplicates on title and remove 
    - remove unimportant columns like img and datatime 
    - when the above steps are done, continue converting the excel to json 
    - find out further steps for an efficient analysis in Swiss Tribeleaders and their influence 
    - maybe check articles for other mentioned personas that could be candidates for the tribe 
"""
















