'''
    File name: generate_greenery.py
    Author: Jakub Lichman
    Date created: 5/6/2018
    Python Version: 3.6.3
'''

from GreeneryDetector import GreeneryDetector
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

MAP = 'Zurich'                          # path to image without suffix
SATELLITE_MAP = MAP + '.png'            # path to image with suffix
NEW_MAP = MAP + '_greenery.png'         # path to new image with detected greenery

# create detector and save image with detected greenery
detector = GreeneryDetector(SATELLITE_MAP)
#detector.detect()                      # simple stupid detector 
#locations = detector.detectWithCV()    # detector with help of openCV + returns binary matrix where 1 => greenery, 0 otherwise
locations = detector.detectWithCVSmoothing(10)
                                        # same as detectWithCV but does the smoothing e.g. in radius(passed as parameter) computes
                                        # influence of green pixels to non green onces -> see visualization
detector.saveImage(NEW_MAP)             # saves image with detected greenery
# print (locations)
vis_l = locations * 255                 # shift to the range (0, 255)
vis_l = vis_l.astype(int)               # convert to int
plt.imshow(locations, interpolation='nearest', cmap=cm.Greys_r)
plt.show()                              # show matrix
im = Image.fromarray(vis_l.astype('uint8'))
im.save("temp.png")
