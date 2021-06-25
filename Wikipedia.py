# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:16:27 2021

@author: vikto
"""

import pandas as pd
import wikipediaapi
import pywikibot as pw


wiki_wiki = wikipediaapi.Wikipedia(
        language='de',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

thoughtleaders = ['Aaron Troschke', 'Adolf Muschg', 'Alice Schwarzer', 'Aline Wanner', 'Andres Veiel',
                 'Anne Siemens', 'Anne Will', 'Annemarie Piper', 'Annika Brockschmidt', 'Axel Honneth',
                 'Barbara Bleisch', 'Benedikt XVI.', 'Bernhard Waldenfels', 'Carina Kontio', 'Charles Lewinsky', 
                 'Christian Drosten', 'Christian Walther', 'Christoph Keller', 'Clemens Fuest', 'Deniz Utlu', 
                 'Dorothea Baur', 'Elham Manea', 'Felix Dachsel', 'Florian Aigner', 'Flurina Badel', 'Frank Thelen', 
                 'Friedrich Ani', 'Georg Diez', 'Günther Jauch', 'Günther Witzany', 'Hans-Werner Sinn', 'Hazel Brugger', 
                 'Heike Behrend', 'Herta Müller', 'Isabella Eckerle', 'Jan Böhmermann', 'Jan Fleischhauer', 'Jan Philipp Reemtsma', 
                 'Jasmina Kuhnke', 'Jochen Arlt', 'Jochen Wegner', 'Joko Winterscheidt', 'Jonas Lüscher', 'Joyce Ilg', 'Julia Jäkel',
                 'Julia Zeh', 'Julian Reichelt', 'Jürg Halter', 'Jürgen Habermas', 'Kai Diekmann', 'Karl Lauterbach', 
                 'Kathrin Passig', 'Katja Gentinetta', 'Katja Rost', 'Klaas Heufer Umlauf', 'Lena-Sophie Müller', 'Linus Schöpfer', 
                 'Ludwig Hasler', 'Luisa Neubauer', 'Lukas Bärfuss', 'Mai Thi Nguyen-Kim', 'Maja Goepel', 'Malcolm Ohanwe', 
                 'Marietta Slomka', 'Mario Adorf', 'Markus Gabriel', 'Martin Meyer', 'Martin R. Dean', 'Melanie Brinkmann', 'Michael Roes', 
                 'Michael Zürn', 'Milena Moser', 'Milo Rau', 'Miriam Meckel', 'Mirjam Fischer', 'Mo Asumang', 'Natascha Hoffner', 
                 'Natascha Strobl', 'Nikolaus Blome', 'Norbert Gstrein', 'Oliver Welke', 'Patti Basler', 'Peter Bichsel', 
                 'Peter Bieri', 'Peter Sloterdijk', 'Peter Spork', 'Philipp Huebl', 'Pinar Atalay', 'Rainer Moritz', 'Rana Ahmad', 
                 'Rezo', 'Richard David Precht', 'Robert Pfaller', 'Rolf Dobelli', 'Roman Bucheli', 'Ronnie Grob', 'Ronya Othmann', 
                 'Sascha Lobo', 'Sibylle Berg', 'Silvia Tschui', 'Simon Bärtschi', 'Sophie Passmann', 'Stephan Anpalagan', 
                 'Tamara Wernli', 'Teo Pham', 'Thomas Hürlimann', 'Tijen Onaran', 'Ueli Mäder', 'Ulrich Wickert', 'Volker Quaschning', 
                 'Werner Herzog', 'Wilhelm Schmid', 'Yael Meier', 'Zora del Buono']

df = pd.DataFrame({'Thoughtleader': 'no one', 'Backlinks': [0], 'Links': [0], 'Awards': [0], 'Publications': [0]})

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
        
        publications_2020 = 0
        publications_2021 = 0
     
        werke = ['Prosa', 'Sachbuch', 'Als Herausgeber', 'Als Herausgeberin', 'Al Übersetzer', 'Theaterstücke', 'Übersetzungen',
                         'Hörspiele', 'Hörbücher', 'Radiomoderationen', 'Podcast', 
                         'TV-Moderationen', 'Veröffentlichungen', 'Bücher', 'Hörbücher', 
                         'Singles', 'Alben', 'Bühnenprogramme', 'Ausführender Produzent', 
                         'Gastauftritte', 'Ausstellung', 'Fernsehen', 'Kino', 'Synchronrollen', 'Filme',
                         'Moderation', 'Serien', 'Fernsehshows', 'Dokumentationen', 
                         'Moderation', 'Radio', 'Podcast', 'Sonstiges', 'Reporter / Moderator', 'Als Gast / Teilnehmer', 
                         'Chronologisches Werkverzeichnis', 'Debatte', 'Als Autorin', 'Monographien', 'Wissenschaftliche Fachartikel (Auswahl)',
                         'Sonstige Artikel (Auswahl)']
        for s in sections:
    
            if s.title == 'Werke' or s.title == 'Werk' or s.title == 'Veröffentlichungen' or s.title == 'Veröffentlichungen (Auswahl)' or s.title == 'Publikationen' or s.title == 'Filmografie' or s.title == 'Fernsehen' or s.title == 'Schriften':  
                
                publications_2020 += s.text.count("2020")
                publications_2021 += s.text.count("2021") 
                
                sections = s.sections
                
                for s in sections:
                    for w in werke:
                        if s.title == w:
                            #print(s.title)
                            if s.title == 'Veröffentlichungen':
                                sections = s.sections
                                #print(sections)
                                for s in sections:
                                    for w in werke:
                                        if s.title == w:
                                            #print(s.title)
                                            publications_2020 += s.text.count("2020")
                                            publications_2021 += s.text.count("2021") 
                            else:
                                publications_2020 += s.text.count("2020")
                                publications_2021 += s.text.count("2021")

                
        publications_20_21 = publications_2020 + publications_2021
                
        return publications_20_21
                    
    backlinks = backlinks(thoughtleader)
    links = print_links(p_wiki)
    auszeichnungen = print_amount_of_auszeichnungen(p_wiki.sections)
    publications = print_amount_of_publications(p_wiki.sections)
    
    d = {'Thoughtleader': thoughtleader, 'Backlinks': [backlinks], 'Links': [links], 'Awards': [auszeichnungen], 'Publications': [publications]}
    df_2 = pd.DataFrame(data=d)
    
    df = pd.concat([df, df_2])

df = df.iloc[1:]
df.to_csv("Thoughtleader_Wikipedia.csv", encoding='utf-8')    

print(df)