#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:38:52 2021

@author: janko
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

url = "https://coinmarketcap.com/historical/"
response = requests.get(url, headers={'User-agent': 'bot 2'}, timeout=5)

soup = BeautifulSoup(response.content, "html.parser")

vol = pd.DataFrame()
close = pd.DataFrame()
supply = pd.DataFrame()

historical_data = {}
e = []

for link in soup.find_all('a', href=True):
    if 'historical' in link['href'] and '20' in link['href']:
        hist_link = "https://coinmarketcap.com" + link['href']
        tries = 0
        found = 0
        while tries <= 5 and found == 0:
            try:
                df = pd.read_html(hist_link)
                for t in df:
                    if len(t.index) > 3:
                        found = 1
                        print(hist_link)
                        historical_data[hist_link.split('/')[-2]] = t
                        add = t[['Name', 'Price']].T
                        add.columns = t.Name
                        add = add.drop(labels='Name')
                        add.index = [hist_link.split('/')[-2]]
    
                        if 'Volume (24h)' in t.columns:
                            addv = t[['Name', 'Volume (24h)']].T
                            addv.columns = t.Name
                            addv = addv.drop(labels='Name')
                            addv.index = [hist_link.split('/')[-2]]
                            addv = pd.DataFrame(addv.T).drop_duplicates(keep='first').T
                            if vol.empty:
                                vol = addv.copy()
                            else:
                                addv = addv.dropna(axis = 1)
                                for a in addv.columns:
                                    if a != "Tickets":
                                        if type(addv.loc[addv.index[0], a]) == str:
                                            vol.loc[addv.index[0], a] = addv.loc[addv.index[0], a]
                                        else:
                                            vol.loc[addv.index[0], a] = addv.loc[addv.index[0], a].values[0]
    
                        adds = t[['Name', 'Circulating Supply']].T
                        adds.columns = t.Name
                        adds = adds.drop(labels='Name')
                        adds.index = [hist_link.split('/')[-2]]
    
                        if close.empty:
                            close = add.copy()
                            supply = adds.copy()
                        else:
                            close = pd.concat([close, add], axis=0)
                            supply = pd.concat([supply, adds], axis=0)
    
                    sleep(1)
                    tries = tries + 1
            except:
                tries = tries + 1


close.to_csv('cm_close.csv')
supply.to_csv('cm_supply.csv')
vol.to_csv('cm_vol.csv')