# -*- coding: utf-8 -*-
"""
@author: Florian Koch
@license: All rights reserved
"""
import pandas as pd
import json

with open('../../data/city_of_zurich/aussichtspunkt.json') as data_file:
  data = json.load(data_file)
  df = pd.io.json.json_normalize(data, ['features', ['geometry', 'coordinates']],['name', ['features', 'properties', 'name']])
  df1 = df[::2]
  df1.columns = ['E', 'type', 'name']
  df2 = df[1::2]
  df2.columns = ['N', 'type', 'name']
  df = pd.merge(df1,df2,how='outer', on=['name', 'type'])
  df = df[['E', 'N', 'name', 'type']]
  df.type = 'Sighting Point'

# print(df)
df.to_csv('../../data/prepared/sighting_point.csv')
