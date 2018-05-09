'''
    File name: generate_greenery.py
    Author: Jakub Lichman
    Date created: 5/6/2018
    Python Version: 3.6.3
'''

from GreeneryDetector import GreeneryDetector
import numpy as np 

MAP = 'Zurich'                          # path to image without suffix
SATELLITE_MAP = MAP + '.png'            # path to image with suffix
NEW_MAP = MAP + '_greenery.png'         # path to new image with detected greenery

# create detector and save image with detected greenery
detector = GreeneryDetector(SATELLITE_MAP)
#detector.detect()
locations = detector.detectWithCV()
detector.saveImage(NEW_MAP)
