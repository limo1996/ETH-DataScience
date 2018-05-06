from GreeneryDetector import GreeneryDetector
import numpy as np 

MAP = 'Zentrum'                         # path to image without suffix
SATELLITE_MAP = MAP + '.png'            # path to image with suffix
NEW_MAP = MAP + '_greenery.png'         # path to new image with detected greenery

# create detector and save image with detected greenery
detector = GreeneryDetector(SATELLITE_MAP)
detector.detect()
detector.saveImage(NEW_MAP)
