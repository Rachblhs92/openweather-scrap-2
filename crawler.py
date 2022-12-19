#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 01:10:30 2021

@author: &&
"""

from IPython.display import Image
from IPython.core.display import HTML
import os
import csv
from termcolor import colored, cprint
Image(url= "weather.png")
import datetime
import json
import urllib.request
import pandas as pd
import json
import pandas as pd
from pandas.io.json import json_normalize #package for flattening json in pandas df



def url_builder(city_id,city_name,country):
    user_api = '2f1ada7ea283d4d805334d73f23d94f9' # Obtain yours form: http://openweathermap.org/
    unit = 'metric' # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    if(city_name!=""):
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' # "http://api.openweathermap.org/data/2.5/weather?q=Tunis,fr
        full_api_url = api + str(city_name) +','+ str(country)+ '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id=' # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    
    return full_api_url




def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict





def data_organizer(raw_api_dict):
    data = dict(
    city=raw_api_dict.get('name'),
    country=raw_api_dict.get('sys').get('country'),
    temp_max=raw_api_dict.get('main').get('temp_max'),
    temp_min=raw_api_dict.get('main').get('temp_min'),
    )
    return data



def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('')
    print('Température à : {}, {}:'.format(data['city'], data['country']))
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('---------------------------------------')



def WriteCSV(data):
    with open('weatherOpenMap.csv', 'a') as f: # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)

def ReadCSV():
    try:
    #ouverture de fichier en mode lecture en specifiant le encodage
        with open("weatherOpenMap.csv",'r') as Fichier:
        #lecture – utilisation du parseur csv en specifiant délimiteur
            csv_contenu = csv.reader(Fichier,delimiter=",")
            reader = csv.DictReader(Fichier)
            dic={}
        for row in reader:
            print (row['city'])
            dic.update(row)
            #fermeture du fichier avec la méthode close()
            Fichier.close()
        return dic
    except IOError:
        print("Fichier n'est pas trouvé")




#load json object



def getVilles():
    with open('city.list.json') as f:
        d = json.load(f)
        villes=pd.DataFrame(d)
    return villes

villes = getVilles()
ville_fr = villes[villes["country"]=='FR']['id']

import time

if __name__ == '__main__':
    try:
        city_name=''
        country='FR'
        compteur = 0
        
        for ville_id in ville_fr :
            city_id= ville_id
            #Generation de l url
            print(colored('Generation de l url ', 'red',attrs=['bold']))
            url=url_builder(city_id,city_name,country)
            #Invocation du API afin de recuperer les données
            print(colored('Invocation du API afin de recuperer les données', 'red',attrs=['bold']))
            data=data_fetch(url)
            #Formatage des données
            print(colored('Formatage des donnée', 'red',attrs=['bold']))
            data_orgnized=data_organizer(data)
            #Affichage de données
            print(colored('Affichage de données ', 'red',attrs=['bold']))
            data_output(data_orgnized)
            print(colored('Enregistrement des données à dans un fichier CSV ', 'green',attrs=['bold']))
            WriteCSV(data_orgnized)
            #Temporisation 1.2 seconde pour ne pas dépasser les 60 requettes par minutes 
            time.sleep(0.2)
            print(colored('Lecture des données à partir un fichier CSV ', 'green',attrs=['bold']))
            #Lecture des données a partir de fichier CSV
            #data=ReadCSV()
            #print(colored('Affichage des données lues de CSV ', 'green',attrs=['bold']))
            #Affichage des données
            #data_output(data)
        compteur += 1
            
    except IOError:
        print('no internet')
        # print('Le nombre de villes affichées est de : '+ str(compteur)

