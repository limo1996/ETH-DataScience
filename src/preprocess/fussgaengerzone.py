# -*- coding: utf-8 -*-
"""
@author: Florian Koch
@license: All rights reserved
"""
import pandas as pd
import numpy as np
import json

with open('../../data/city_of_zurich/fussgaengerzone.json') as data_file:
  data = json.load(data_file)
  df = pd.io.json.json_normalize(data, ['features', ['geometry', 'coordinates']],['name', ['features', 'properties', 'zonenname'], ['features', 'properties', 'bestehend']])

df.columns = ['coordinate array', 'type', 'name', 'present']
list = np.array([[]])
for i in range(len(df)):
  list = np.append(list, df['coordinate array'][i])
list = np.reshape(list, (len(list)//2, 2))
# print(list)
df = pd.DataFrame(data=list,columns=['East', 'North'])
# print(df)
df.to_csv('../../data/prepared/pedestrian_zone.csv')
