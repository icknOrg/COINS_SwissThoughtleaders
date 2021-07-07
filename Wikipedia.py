# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:16:27 2021

@author: vikto
"""

import pandas as pd
import wikipediaapi
import pywikibot as pw

#settings
wiki_wiki = wikipediaapi.Wikipedia(
        language='de',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

#get data of .xlsx file
tl = pd.read_excel('COINs Intelektuellen-Ranking.xlsx', index_col=0, dtype=str)
thoughtleaders = tl['Wikipedia'].tolist()
thoughtleaders = [x for x in thoughtleaders if pd.notnull(x)]
print(thoughtleaders)

#initialize dataframes
df = pd.DataFrame({'Thoughtleader': 'no one', 'Backlinks': [0], 'Links': [0], 'Awards': [0], 'Publications': [0]})
df_2 = pd.DataFrame({'Thoughtleader': 'no one', 'Wikipedia_score': [0]})

for thoughtleader in thoughtleaders:
    
    print(thoughtleader)
    p_wiki = wiki_wiki.page(thoughtleader)
    
    
    
    #get the backlinks
    def backlinks(thoughtleader):
        backlinks_list = []

        for item_backlink in pw.Page(pw.Site('de', 'wikipedia'), thoughtleader).backlinks(follow_redirects=False):
            backlinks_list.append(item_backlink.title())
    
        return(len(backlinks_list))
    
    
    
    #get the links on the page
    def print_links(page):
            
        links = page.links
        amount_of_links = 0
        for title in sorted(links.keys()):
            amount_of_links = amount_of_links + 1
        return amount_of_links
    
    #print the different sections
    #def print_sections(sections, level=1):
     #       for s in sections:
      #              print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
       #             print_sections(s.sections, level + 1)
    
    #print_sections(p_wiki.sections)     
    
    
    
    #get the amount of won prices 
    def print_amount_of_auszeichnungen(sections, level=1):
        
        auszeichnungen_20_21 = 0
        
        for s in sections:
            if s.title == "Auszeichnungen" or s.title == "Auszeichnung" or s.title == 'Auszeichnungen und Nominierungen':

                auszeichnungen_2020 = s.text.count('2020:')
                auszeichnungen_2021 = s.text.count('2021:')
                auszeichnungen_20_21 = auszeichnungen_2020 + auszeichnungen_2021
    
        return auszeichnungen_20_21
                    
            
    
    #get the amount of publications
    def print_amount_of_publications(sections):
        
        publications_20_21 = 0
     
        werke = ['Werk', 'Publikation', 'Prosa', 'Fernsehen', 'Schrift', 'Sach', 'Als', 'Theater', 'Übersetzung',
                 'Hör', 'Radio', 'Podcast', 'Veröffentlichung', 'Buch', 'Diskografie',
                 'CD', 'Bücher', 'Krimi', 'Romane', 'Bühne', 'Singles', 'Alben', 
                 'Ausführender Produzent', 'Ausführende Produzentin', 'Gastauftritte', 
                 'Ausstellung', 'Kino', 'Synchronrollen', 'Film', 'Moderation', 'Serien', 
                 'Fernsehshows', 'Dokumentationen', 'Fernsehauftritte', 'Sonstiges', 
                 'Reporter / Moderator', 'Video', 'Artikel', 'Chronologisch', 'Debatte', 
                 'Monographien', 'Wissenschaftliche Fachartikel', 'Literatur', 'Anthologien', 
                 'Herausgabe', 'titel', 'Originalausgaben', 'Politisch', 'kritik', 'Kritik']
        
        #Looking at the first level
        for s in sections:
            for w in werke:
                if w in s.title:  
                    print("1. Level: ",s.title)
                    partitioned_string = s.text.split('\n')
                    print(partitioned_string)
                    for line in partitioned_string:
                        
                        if line.count("2020") > 0 or line.count("2021") > 0:
                            
                            publications_20_21 += 1
                    
                    #Looking at the second level
                    sub_sections = s.sections
                    
                    for sub in sub_sections:
                        for w in werke:
                            if w in sub.title:
                                    print("2. Level: ",sub.title)
                                    partitioned_string = sub.text.split('\n')
                                    print(partitioned_string)
                                    for line in partitioned_string:
                                        if line.count("2020") > 0 or line.count("2021") > 0:
                                            
                                            publications_20_21 += 1
                                            
                                    #Looking at the third level
                                    sub_sub_sections = sub.sections
                                    
                                    #print(sections)
                                    for sub_sub in sub_sub_sections:
                                        for w in werke:
                                            if w in sub_sub.title:
                                                 print("3. Level: ", sub_sub.title)
                                                 partitioned_string = sub_sub.text.split('\n')
                                                 for line in partitioned_string:
                                                     if line.count("2020") > 0 or line.count("2021") > 0:
                                                         
                                                         publications_20_21 += 1
                                    
                
        return publications_20_21
                    
    backlinks = backlinks(thoughtleader)
    links = print_links(p_wiki)
    auszeichnungen = print_amount_of_auszeichnungen(p_wiki.sections)
    publications = print_amount_of_publications(p_wiki.sections)
    
    #calculate the wikipedia score by adding all up
    wikipedia_score = links + backlinks + 100*auszeichnungen + 100*publications
    
    d = {'Thoughtleader': thoughtleader, 'Backlinks': [backlinks], 'Links': [links], 'Awards': [auszeichnungen], 'Publications': [publications]}
    df_wikipedia_values = pd.DataFrame(data=d)
    df = pd.concat([df, df_wikipedia_values])
    
    d_2 = {'Thoughtleader': thoughtleader, 'Wikipedia_score': [wikipedia_score]}
    df_wikipedia_score = pd.DataFrame(data=d_2)
    df_2 = pd.concat([df_2, df_wikipedia_score])



df = df.iloc[1:]
df_2 = df_2.iloc[1:]  

#Normalize score with min-max normalization
df_2['Wikipedia_score']=(df_2['Wikipedia_score']-df_2['Wikipedia_score'].min())/(df_2['Wikipedia_score'].max()-df_2['Wikipedia_score'].min())

df_2.to_csv("Thoughtleader_Wikipedia.csv", encoding='utf-8')

print(df)
print(df_2)

def get_wikipedia(): 
    global wikipedia; 
    wikipedia = pd.DataFrame(df)
    return wikipedia; 
    





