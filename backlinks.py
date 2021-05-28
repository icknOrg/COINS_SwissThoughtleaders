# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:49:59 2021

@author: vikto

    get backlinks of Wikipedia pages
"""

import pywikibot as pw
backlinks_list = []

for item_backlink in pw.Page(pw.Site('de', 'wikipedia'), "Sibylle Berg").backlinks(follow_redirects=False):
    backlinks_list.append(item_backlink.title())
    
print(backlinks_list)
print(len(backlinks_list))