# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 21:00:29 2021

@author: vikto
"""


import wikipedia

wikipedia.set_lang('de')

print(wikipedia.page('Jan Böhmermann').section('TV-Moderationen'))


print(p_wiki.text)


import wikipediaapi


wiki_wiki = wikipediaapi.Wikipedia(
        language='de',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

p_wiki = wiki_wiki.page("Sibylle Berg")

print(p_wiki.text)

#print the different sections
def print_sections(sections, level=0):
        for s in sections:
                print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
                print_sections(s.sections, level + 1)

print_sections(p_wiki.sections)     

#get the amount of won prices 
def print_amount_of_auszeichnungen(sections, level=0):
        for s in sections: 
            if s.title == "Auszeichnungen" or s.title == "Auszeichnung":
                print(s.text)
                print("Amount of Auszeichnungen: ", (s.text.count("\n")+1))

print_amount_of_auszeichnungen(p_wiki.sections)

#get the amount of publications
def print_amount_of_auszeichnungen(sections, level=0):
        for s in sections: 
            if s.title == "Veröffentlichungen" or s.title == "Werke":
                print(s.text)
                print("Amount of Veröffentlichungen or Werke: ", (s.text.count("\n")+1))

print_amount_of_auszeichnungen(p_wiki.sections)