#!/usr/bin/env python
# coding: utf-8

# In[134]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
import re
import requests


# In[135]:


def awards_in_20_21(url):
    """
    This function prints whether an award is listed for 2020/21 for the person whose Wikpedia link is passed.
    ----------------------------------------------
    :param
        url (String): Url for Wikipedia site.
    """
    try: 
        url = url
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
    

    #for team in teams:
    #    print(team.string)
    
    uls = []
    for nextSibling in teams.findNextSiblings():
        if nextSibling.name == 'li':
            uls.append(nextSibling)
       
    #for li in uls:
    #    li.text.encode("utf-8")
        
    if any("2020" in s for s in uls) or any("2021" in s for s in uls):
        print("Has won an award in 2020/21!")
        return
    
    if any("2020" in s for s in uls[-1]) or any("2021" in s for s in uls[-1]):
        print("Has won an award in 2020/21!")


# In[136]:


test_url = 'https://de.wikipedia.org/wiki/Mai_Thi_Nguyen-Kim'


# In[137]:


awards_in_20_21(test_url)


# In[138]:


def publications_in_20_21(url):
    """
    This function prints whether a publication is listed for 2020/21 for the person whose Wikpedia link is passed.
    ----------------------------------------------
    :param
        url (String): Url for Wikipedia site.
    """
    
    try: 
        url = url
        html = urlopen(url) 
        soup = BeautifulSoup(html, 'html.parser')
    except:
        print("Passed url is not valid.")
        return
    
    heading = soup.find(id=re.compile("Veröffentlichungen"))

    
    try: 
        teams = heading.find_next('li')
    except:
        print("No publication section found on german wikipedia.")
        return

    #for team in teams:
    #    print(team.string)
    
    uls = []
    for nextSibling in teams.findNextSiblings():
        if nextSibling.name == 'li':
            uls.append(nextSibling)
       
    #for li in uls:
    #    li.text.encode("utf-8")
        
    if any("2020" in s for s in uls) or any("2021" in s for s in uls):
        print("Has published sth. in 2020/21!")
        return
    
    if any("2020" in s for s in uls[-1]) or any("2021" in s for s in uls[-1]):
        print("Has published sth. in 2020/21!")


# In[139]:


publications_in_20_21(url)


# In[ ]:




