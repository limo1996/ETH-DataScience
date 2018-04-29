from PIL import Image
import numpy as np
from numpy import *
import IntensityFinder
from IntensityFinder import IntensityFinder, InfluenceType
from contour.ContourDrawer import ContourDrawer, Settings, Coordinate

SOURCE = '../data/prepared/sighting_point.csv'
ZURICH_MAP_LOC = "staticmap.jpeg"
RESULT = 'sighting_point.png'
OVERLAY_RESULT = 'sighting_point_overlay.png'
RADIUS = 150
#FUNCTION = IntensityFinder.exponential2
INFLUENCE_TYPE = InfluenceType.CLOSEST_POINT
TO_OVERLAY = ["sighting_point.png"]

def compute_heatmap(intensity_finder_obj, long_left, long_right, lat_top, lat_bot, image, result_path,  radius, function, influence_type):

    # Get the size of the image
    width, height = image.size

    # Get the dimensions
    lat = lat_top - lat_bot
    long = long_right - long_left

    # Get the steps to get the corresponding gps position for each pixel
    lat_step = lat/height
    long_step = long/width

    # Load a heatmap of the same dimensions
    heatMap = image
    pix = heatMap.load()

    #heatMap.save(result_path)
    
    # Set the values of each pixel
    for i in range(width):
        for j in range(height):
            if InfluenceType.ALL_POINTS == INFLUENCE_TYPE:
                res = int(255 * sum(intensity_finder_obj.get_intensity(Coordinate(lat_top-j*lat_step, long_left+i*long_step), radius, intensity_finder_obj.exponential, influence_type)))
            else :
                res = int(255 * (intensity_finder_obj.get_intensity(Coordinate(lat_top-j*lat_step, long_left+i*long_step), radius, intensity_finder_obj.exponential, influence_type)))
            
            pix[i,j] = (res, 0 , 0)

    # Save the heatmap at correspondin path
    heatMap.save(result_path)

def get_zurich_map():

    # Set bounds
    long_right = 8.594724
    long_left = 8.484963
    lat_top = 47.42177
    lat_bot = 47.347436

    # Get image
    im = Image.open(ZURICH_MAP_LOC)

    # Return everything
    return long_left, long_right, lat_top, lat_bot, im

def get_map(source_path, result_path, radius, function, influence_type):

    # Use ContourDrawer to get data
    drawer = ContourDrawer()
    drawer.load_data(SOURCE , ',', [2, 1])

    # Initialise Intensity Finder
    finder = IntensityFinder(drawer.get_data())
    #finder = IntensityFinder([Coordinate(47.404802, 8.501339), Coordinate(47.404802, 8.581339)])

    # Get Zurich map and the latitude/longitude bounds
    long_left, long_right, lat_top, lat_bot, image = get_zurich_map()

    # Create Heatmap
    compute_heatmap(finder, long_left, long_right, lat_top, lat_bot, image, RESULT, RADIUS, IntensityFinder.exponential2 , INFLUENCE_TYPE)

def combine_maps(other_to_overlayy, result_path):

    image = Image.open(ZURICH_MAP_LOC)
    result = image

    others = [(asarray(Image.open(i)) / len(other_to_overlayy)) for i in other_to_overlayy]
    other = others[0]
    for i in range(len(others)):
        if i != 0:
            other = other + others[i]
    result = asarray(image) * 0.4
    other = other * 0.6

    result = (result + other).astype('uint8')
    result = Image.fromarray(result)

    result.save(result_path)

#get_map(SOURCE, RESULT, RADIUS, IntensityFinder.exponential2, INFLUENCE_TYPE)
#combine_maps(TO_OVERLAY, OVERLAY_RESULT)


