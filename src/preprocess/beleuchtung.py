# -*- coding: utf-8 -*-
"""
@author: Florian Koch
@license: All rights reserved
"""
import pandas as pd
import json

with open('../../data/Öffentliche Beleuchtung der Stadt Zürich/beleuchtung.json') as data_file:
  data = json.load(data_file)
  df = pd.io.json.json_normalize(data, ['features', ['geometry', 'coordinates']],['name', ])
  df.columns = ['E', 'N', 'name']
  df.name = 'illumination'

df.to_csv('../../data/prepared/illumination.csv')
