'''
    File name: ContourGradients.py
    Author: Jakub Lichman
    Date created: 4/10/2018
    Python Version: 3.6.3
'''

from enum import Enum

class HeatType(Enum):
    """ Enumaration that lists gradient possibilities for heat map """
    RED_TO_GREEN = "RED_TO_GREEN",
    GREEN_TO_RED = "GREEN_TO_RED",
    GREEN_TO_EVERYTHING_RED = "GREEN_TO_EVERYTHING_RED",
    GREEN_TO_EVERYTHING_RED_CENTER_EMPTY = "GREEN_TO_EVERYTHING_RED_CENTER_EMPTY"

# color gradients for heat maps
GRADIENTS = {
    "RED_TO_GREEN_GRADIENT" : [
        (102, 255, 0, 0),           #transparent
        (102, 255, 0, 1),           #green
        (147, 255, 0, 1),
        (193, 255, 0, 1),
        (238, 255, 0, 1),
        (244, 227, 0, 1),
        (249, 198, 0, 1),
        (255, 170, 0, 1),
        (255, 113, 0, 1),
        (255, 57, 0, 1),
        (255, 0, 0, 1)              #red
    ],
    "GREEN_TO_RED_GRADIENT" : [
        (102, 255, 0, 0),           #transparent
        (255, 0, 0, 1),             #red
        (255, 57, 0, 1),
        (255, 113, 0, 1),
        (255, 170, 0, 1),
        (249, 198, 0, 1),
        (244, 227, 0, 1),
        (244, 227, 0, 1),
        (238, 255, 0, 1),
        (193, 255, 0, 1),
        (147, 255, 0, 1),
        (102, 255, 0, 1)            #green
    ],
    "GREEN_TO_EVERYTHING_RED_GRADIENT" : [
        (255, 0, 0, 1),             #red
        (255, 57, 0, 1),
        (255, 113, 0, 1),
        (255, 170, 0, 1),
        (249, 198, 0, 1),
        (244, 227, 0, 1),
        (244, 227, 0, 1),
        (238, 255, 0, 1),
        (193, 255, 0, 1),
        (147, 255, 0, 1),
        (102, 255, 0, 1)            #green
    ],
    "GREEN_TO_EVERYTHING_RED_CENTER_EMPTY_GRADIENT" : [
        (255, 0, 0, 1),             #red
        (255, 57, 0, 1),
        (255, 113, 0, 1),
        (255, 170, 0, 1),
        (249, 198, 0, 1),
        (244, 227, 0, 1),
        (244, 227, 0, 1),
        (238, 255, 0, 1),
        (193, 255, 0, 1),
        (147, 255, 0, 1),
        (102, 255, 0, 1),           #green
        (102, 255, 0, 0)            #transparent
    ]
}

def getGradient(gradient_type: HeatType):
    """ Returns heat gradient for map drawing according to provided heat type. """
    return GRADIENTS['{0}_GRADIENT'.format(gradient_type.name)]