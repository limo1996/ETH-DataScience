'''
    File name: IntensityFinder.py
    Author: Jakub Lichman
    Date created: 4/11/2018
    Python Version: 3.6.3
'''

from math import sin, cos, sqrt, atan2, radians, exp
from contour.ContourDrawer import Coordinate
from scipy.spatial import KDTree

from enum import Enum
import numpy as np

class InfluenceType(Enum):
    """ Represents the influence type for intensity. Influence can come either 
        from all points within a range or from the closest one. """
    ALL_POINTS = np.inf,
    CLOSEST_POINT = 1

class IntensityFinder(object):
    """
    Class that is able to find intensity on a map effectively.
    Effective usage is to create class once from data points and than to query it multiple times.
    """
    def __init__(self, data):
        """ Creates new instance of IntensityFinder from sequence of data points """
        pts = [i.to_tuple() for i in data]
        self.tree = KDTree(pts)

    def get_intensity(self, coordinate: Coordinate, radius: int, func, influenceType: InfluenceType):
        """ 
        Returns intensity on the given point.
        
        Params:
            - coordinate: coordinates of point to query.
            - radius: radius of influence of data points provided in contructor. 
            - func: function that takes as input radius and distance from closest point
                    and returns intensity for given point. This object contains several
                    functions that can be passed: {exponential, exponential2, linear, quadratic}
        """
        converted_radius = self.convert_radius(radius)
        coord = coordinate.to_tuple()
        nearest_points = self.get_nearest_points(coord, converted_radius, influenceType)
        distances = self.compute_distances(coord, nearest_points)
        if isinstance(distances, list):
            #print ('distances: ', distances)
            #print ('max: {0} min: {1}'.format(func(radius, 0), func(radius, radius)))
            return [func(radius, i) for i in distances]
        else:
            if distances > radius:
                return 0
            f_max = func(radius, 0)
            f_min = func(radius, radius)
            return self.normalize(f_min, f_max, func(radius, distances))

    def get_nearest_points(self, coord, radius: int, influenceType: InfluenceType):
        """ returns nearest point(s) to coord according to influenceType and radius """
        if influenceType == InfluenceType.CLOSEST_POINT:
            return self.tree.data[self.tree.query(coord)[1]]
        else:
            dsize = len(self.tree.data)
            #print(np.transpose(self.tree.query(coord, k=10000, distance_upper_bound=radius)[1]))
            return [self.tree.data[p] for p in filter(lambda x: x < dsize and x >= 0, self.tree.query(coord, k=10000, distance_upper_bound=radius)[1])]

    def convert_radius(self, radius):
        """ Radius is provided in meters but coordiantes are (lat, lon) so we need to translate distance in meters to distance between 
            two coordinates ad float. cca 1 meter is 0.00001 euclidean distance between coordinates """
        return radius * 0.00001
        
    def exponential(self, radius, x):
        """ Exponentially decreasing function: f(x) = ax^1/(x+a) where a = radius """
        return radius * 2**(1/(x + radius))

    def exponential2(self, radius, x):
        """ Another exponentially decreasing function with euler number as base.
            defined as f(x) = ax^-x  where a = radius """
        return radius * exp(-x)

    def linear(self, radius, x):
        """ Linearly decreasing function: f(x) = -2x + 2a  where a = radius"""
        return -radius*x + 2*radius

    def quadratic(self, radius, x):
        """ Quadratically decreasing function on interval <0,a>. 
            defined as: f(x) = (x - a)^2 where a = radius """
        return (x - radius)**2

    def normalize(self, f_min, f_max, x):
        """ normalizes provided data """
        return (x - f_min)/(f_max - f_min)

    def compute_distances(self, coord1, coordinates):
        """ computes distances between coord1 and all coordinates """
        if isinstance(coordinates, list):
            return [self.compute_distance(coord1, coord) for coord in coordinates]
        else:
            return self.compute_distance(coord1, coordinates)

    def compute_distance(self, coord1, coord2):
        """ computes distance in meters between two coordinates given in form of an array """
        assert len(coord1) == 2 and len(coord2) == 2

        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(coord1[0])
        lon1 = radians(coord1[1])

        lat2 = radians(coord2[0])
        lon2 = radians(coord2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        #print ('distance between {0} and {1} is {2}'.format(coord1, coord2, R * c * 1000))
        return R * c * 1000
