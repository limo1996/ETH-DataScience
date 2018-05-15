'''
    File name: GreeneryDetector.py
    Author: Jakub Lichman
    Date created: 5/6/2018
    Python Version: 3.6.3
'''

from PIL import Image
from multiprocessing import Pool

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class GreeneryDetector:
    """ Detects greenery in the image """
    
    def __init__(self, path):
        """ Creates new instance of GreeneryDetector from image which location is specified by path parameter """
        img = Image.open(path)
        self.pixels = list(img.getdata())
        self.img = img
        self.path = path
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

    def get_data(self, path):
        """ Loads image pixels """
        img = Image.open(path)
        return list(img.getdata())

    def detectWithCV(self):
        """ Detects both forests and grass areas and returns binary matrix indicating their positions. """
        path = self.path
        print(self.pixels[0])
        # lower and upper bounds on greenery detection
        lower_green = np.array([50, 38, 70])
        upper_green = np.array([80, 255, 200])
        lower_forest = np.array([0, 0, 30])
        upper_forest = np.array([120, 255, 50])

        # mask files for forest and green areas detection
        green = 'green_areas.png'
        forest = 'forests.png'
        # create mask images and save them
        self.detectCV(self.path, lower_green, upper_green, green)
        self.detectCV(self.path, lower_forest, upper_forest, forest)
        # load images
        gp = self.get_data(green)
        fp = self.get_data(forest)
        new_pixels = self.pixels
        length = len(self.pixels)
        assert len(gp) == len(fp) == length
        counter = 0
        width, height = self.img.size
        binary_m = np.zeros(length)
        # for each masked pixel check if it is white. If yes than mark 
        # pixel as green and append to binary matrix
        for i in range(0, length):
            if gp[i] == 255:
                new_pixels[i] = (0, 200, 0)
                counter = counter + 1
                binary_m[i] = 1
            i = i+1
        self.new_pixels = new_pixels
        summed = np.add(fp, gp)
        summed = np.minimum(summed, 1)
        #assert np.array_equal(binary_m, summed)
        binary_m = np.reshape(binary_m, (width, height))
        print(binary_m.shape)
        print('{0}/{1} => {2}% of greenery'.format(counter, len(self.pixels), float(counter / len(self.pixels) * 100)))
        return binary_m

    def detectWithCVSmoothing(self, smooth_factor):
        """ Performs detectWithCV together with smoothing of returned matrix. """
        binary_m = self.detectWithCV()
        for i in range(0, smooth_factor):
            self.smooth(binary_m)
        return binary_m

    def smooth(self, matrix):
        """ Smoothes matrix by one level more. """
        width, height = matrix.shape
        for i in range(0, width):
            for j in range(0, height):
                maxx = 0
                if matrix[i,j] == 0:
                    for ii in range(-1, 2):
                        for jj in range(-1, 2):
                            p_i = i + ii
                            p_j = j + jj
                            if 0 <= p_i and p_i < width and 0 <= p_j and p_j < height:
                                if (ii != 0 or jj != 0) and matrix[p_i,p_j] > 0:
                                    maxx = max(maxx, matrix[p_i,p_j])
                        matrix[i,j] = float(maxx / 2)

    def detectCV(self, path, lower_green, upper_green, out_path):
        """ Detects greenery based on intervals provided as params """
        img = cv.imread(path)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # Threshold the HSV image to get only green colors
        mask = cv.inRange(hsv, lower_green, upper_green)
        cv.imwrite(out_path,mask)

    def saveImage(self, path):
        """ Saves new modified image in the location specified by param path """
        self.img.putdata(self.new_pixels)
        self.img.save(path, "PNG")