# -*- coding: utf-8 -*-
"""
@author: Florian Koch
@license: All rights reserved
"""
import pandas as pd
import json

with open('../../data/city_of_zurich/fussgaengerzone.json') as data_file:
  data = json.load(data_file)
  df = pd.io.json.json_normalize(data, ['features', ['geometry', 'coordinates']],['name', ['features', 'properties', 'zonenname'], ['features', 'properties', 'bestehend']])

df.columns = ['coordinate array', 'type', 'name', 'present']
# print(df)
df.to_csv('../../data/prepared/pedestrian_zone.csv')
