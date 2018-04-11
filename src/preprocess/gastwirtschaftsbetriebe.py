# -*- coding: utf-8 -*-
"""
@author: Florian Koch
@license: All rights reserved
"""
import pandas as pd

with open('../../data/Gastwirtschaftsbetriebe per 31.12.2017/gastwirtschaftsbetriebeper20171231.csv') as data_file:
  df = pd.read_csv(data_file,sep=',')

df = df.drop(['Jahr', 'Oeffnungszeit', 'EKoord', 'NKoord', 'KreisSort', 'StatZoneSort', 'QuarSort', 'Betriebsstatus'], axis=1)
# print(df)
df.to_csv('../../data/prepared/restaurants.csv')
