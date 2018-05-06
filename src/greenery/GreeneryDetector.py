from PIL import Image
from multiprocessing import Pool

import matplotlib.pyplot as plt

class GreeneryDetector:
    """ Detects greenery in the image """
    
    def __init__(self, path):
        """ Creates new instance of GreeneryDetector from image which location is specified by path parameter """
        img = Image.open(path)
        self.pixels = list(img.getdata())
        self.img = img
        print('Image pixel count: {0}'.format(len(self.pixels)))

    def update(self, p):
        """ Indicates whether there is greenery at a given pixel """
        return (p[1] > (p[0] + p[2])/2) and p[1] > p[0] - 2 and p[1] > p[2] + 2

    def updatePixel(self, p):
        """ Either assignes pixel to completely green (if there is greenery) or does nothing """
        if self.update(p):
            self.counter = self.counter + 1
            return (0, 255, 0)
        return p
    
    def detect(self):
        """ Detects greenery in the image """
        self.counter = 0
        new_pixels = self.pixels
        i = 0
        for pix in self.pixels:
            new_pixels[i] = self.updatePixel(pix)
            i = i + 1

        updated = self.counter
        self.new_pixels = new_pixels
        print('{0}/{1} => {2}% of greenery'.format(updated, len(self.pixels), float(updated / len(self.pixels) * 100)))

    def saveImage(self, path):
        """ Saves new modified image in the location specified by param path """
        self.img.putdata(self.new_pixels)
        self.img.save(path, "PNG")