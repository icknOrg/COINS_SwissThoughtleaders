#!/usr/bin/env python
# coding: utf-8

# In[34]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
import re
import requests
import pywikibot as pw


# In[53]:


def get_awards(name):
    """
    This function prints whether an award is listed for 2020/21 for the person whose Wikpedia link is passed.
    ----------------------------------------------
    :param
        url (String): Url for Wikipedia site.
    """
    name = name.replace(" ", "_")
    name = name.replace("ö", "%C3%B6")
    name = name.replace("ä", "%C3%A4")
    name = name.replace("ü", "%C3%BC")
    name = name.replace("ß", "%E1%BA%9E")

    first = "https://de.wikipedia.org/wiki/"
    
    url = first+name
    
    try: 
        html = urlopen(url) 
        soup = BeautifulSoup(html, 'html.parser')
    except:
        print("Passed url is not valid.")
        return
    
    heading = soup.find(id=re.compile("Auszeichnung"))

    
    try: 
        teams = heading.find_next('li')
    except:
        print("No award section found on german wikipedia.")
        return
    
    try: 
        teams_p = heading.find_next('p')
    except:
        print("No award section found on german wikipedia.")
        return
    

    #for team in teams:
    #    print(team.string)
    
    uls = []
    for nextSibling in teams.findNextSiblings():
        if nextSibling.name == 'li':
            uls.append(nextSibling)
            
    
    uls_p = []
    for nextSibling in teams_p.findNextSiblings():
        if nextSibling.name == 'p':
            uls_p.append(nextSibling)
    
    #for li in uls:
    #    li.text.encode("utf-8")
        
    if any("2020" in s for s in uls) or any("2021" in s for s in uls):
        print("Has won an award in 2020/21!")
        return
 
    if any("2019" in s for s in uls_p[-1]) or any("2021" in s for s in uls_p):
        print("Has won an award in 2020/21!")
        return
        
    if len(uls)>1:
        if any("2020" in s for s in uls[-1]) or any("2021" in s for s in uls[-1]):
            print("Has won an award in 2020/21!")
            return
        
        if any("2020" in s for s in uls_p[-1]) or any("2021" in s for s in uls_p[-1]):
            print("Has won an award in 2020/21!")
            return


# In[ ]:


def get_publications(name):
    """
    This function prints whether a publication is listed for 2020/21 for the person whose Wikpedia link is passed.
    ----------------------------------------------
    :param
        url (String): Url for Wikipedia site.
    """
    
    name = name.replace(" ", "_")
    name = name.replace("ö", "%C3%B6")
    name = name.replace("ä", "%C3%A4")
    name = name.replace("ü", "%C3%BC")
    name = name.replace("ß", "%E1%BA%9E")
    
    first = "https://de.wikipedia.org/wiki/"
    
    url = first+name
    
    try: 
        html = urlopen(url) 
        soup = BeautifulSoup(html, 'html.parser')
    except:
        print("Passed url is not valid.")
        return
    
    heading = soup.find(id=re.compile("Veröffentlichungen"))

    
    try: 
        teams = heading.find_next('li')
    except:
        print("No award section found on german wikipedia.")
        return
    
    try: 
        teams_p = heading.find_next('p')
    except:
        print("No award section found on german wikipedia.")
        return
    

    #for team in teams:
    #    print(team.string)
    
    uls = []
    for nextSibling in teams.findNextSiblings():
        if nextSibling.name == 'li':
            uls.append(nextSibling)
            
    
    uls_p = []
    for nextSibling in teams_p.findNextSiblings():
        if nextSibling.name == 'p':
            uls_p.append(nextSibling)
    
    #for li in uls:
    #    li.text.encode("utf-8")
        
        
    if any("2020" in s for s in uls) or any("2021" in s for s in uls):
        print("Has published sth. in 2020/21!")
        return
 
    if any("2019" in s for s in uls_p[-1]) or any("2021" in s for s in uls_p):
        print("Has published sth. in 2020/21!")
        return
        
    if len(uls)>1:
        if any("2020" in s for s in uls[-1]) or any("2021" in s for s in uls[-1]):
            print("Has published sth. in 2020/21!")
            return
        
        if any("2020" in s for s in uls_p[-1]) or any("2021" in s for s in uls_p[-1]):
            print("Has published sth. in 2020/21!")
            return


# In[54]:


def get_backlinks(name):
    backlinks_list = []

    for item_backlink in pw.Page(pw.Site('de', 'wikipedia'), name).backlinks(follow_redirects=False):
        backlinks_list.append(item_backlink.title())

    #print(backlinks_list)
    print(len(backlinks_list))
    return len(backlinks_list)


# In[55]:


get_backlinks("Jan Böhmermann")


# In[56]:


get_awards("Jan Böhmermann")


# In[ ]:




