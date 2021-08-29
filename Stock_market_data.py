#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, re, numpy
from bs4 import BeautifulSoup
from itertools import count
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import locale
from unidecode import unidecode

def getInfo(url):
    r = requests.get(url, stream = True)
    if r.status_code != 200:
        raise ValueError
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_plot(company, month, year):
    month = month
    dictionary_days = {
        'january' : 31,
        'february' : 28,
        'march' : 31,
        'april' : 30,
        'may' : 31,
        'june' : 30,
        'july' : 31,
        'august' : 31,
        'september': 30,
        'october' : 31,
        'november' : 30,
        'december' : 31
    }
    dictionary_codes = {
        'january' : '01',
        'february' : '02',
        'march' : '03',
        'april' : '04',
        'may' : '05',
        'june' : '06',
        'july' : '07',
        'august' : '08',
        'september': '09',
        'october' : '10',
        'november' : '11',
        'december' : '12'
    }
    download = []
    values = []
    v = []
    connected = []
    for m in month:
        for i in range(1, dictionary_days[m.lower()] + 1):
            url = f'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date={i}-{dictionary_codes[m.lower()]}-{year}&show_x=Poka%C5%BC+wyniki'
            info = getInfo(url).find_all('tr')
            download.append([m.lower(),info])
    
        for i in download:
            for x in i[1]:
                if x.parent.name == 'tbody':
                    if len(str(download.index(i)+1)) == 1:
                        values.append(x.text.strip().split(sep = '\n') + [f'0{str(int(download.index(i)+1))}-{dictionary_codes[i[0]]}-{year}'])
                    else:
                        values.append(x.text.strip().split(sep = '\n') + [f'{str(int(download.index(i)+1))}-{dictionary_codes[i[0]]}-{year}'])
        download.clear()
    for i in values:
        for x in i:
            x = unidecode(x)
            x = x.replace(',', '.').replace(' ', '')
            try:
                v.append(float(x))
            except:
                v.append(x)
    var = 0
    while True:
        x = v[var:var+9]
        connected.append(x)
        var += 9
        if var >= len(v):
            break
    df = pd.DataFrame(connected)
    df.columns = ['Spolka', 'Waluta', 'C_otw', 'C_max', 'C_min', 'Cena zamknięcia', 'zmiana_%', 'Obrot', 'Data']
    df = df.set_index('Spolka')
    plot = df.loc[company].plot(x='Data', y='Cena zamknięcia', figsize = (20, 10))
    if len(month) > 1:
        plt.title(f'Kurs akcji {company} w okresie {dictionary_codes[month[0].lower()]}-{dictionary_codes[month[-1].lower()]}.{year}', fontsize = 20)
    else:
        plt.title(f'Kurs akcji {company} w {dictionary_codes[month[0].lower()]}.{year}', fontsize = 20)
    
    plt.ylabel('Cena zamknięcia')
    plot.set_ylim(min(df.loc[company, 'Cena zamknięcia']) - 2 * len(month) * (numpy.mean(df.loc[company, 'Cena zamknięcia'])/len(df.loc[company, 'Cena zamknięcia'])), max(df.loc[company, 'Cena zamknięcia']) + 2 * len(month) * (numpy.mean(df.loc[company, 'Cena zamknięcia'])/len(df.loc[company, 'Cena zamknięcia'])))
    plt.legend([company], fancybox=True, framealpha = 1, shadow = True, borderpad = 1)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    price_change = round((df.loc[company, 'Cena zamknięcia'][-1]/df.loc[company, 'Cena zamknięcia'][0]-1)*100,2)
    plt.savefig(f'{company}.png')



get_plot('CDPROJEKT', ['may', 'june'], 2021).  #example for CDPROJEKT in May and June 2021




