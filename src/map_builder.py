from PIL import Image
import numpy as np
from numpy import *
import IntensityFinder
from IntensityFinder import IntensityFinder, InfluenceType
from contour.ContourDrawer import ContourDrawer, Settings, Coordinate

SOURCE = '../data/prepared/driving_prohibited.csv'
ZURICH_MAP_LOC = "staticmap.jpeg"
RESULT = '../report/images/driving_prohibited.png'
HEATMAP = '../report/images/driving_prohibited_heatmap.png'
RADIUS = 70
INFLUENCE_TYPE = InfluenceType.CLOSEST_POINT
#FUNCTION = IntensityFinder.exponential2

OVERLAY_RESULT = '../report/images/combined.png'
COMBINED_HEATMAP = '../report/images/combined_heatmap.png'
TO_OVERLAY = ['../report/images/results/illumination_heatmap_70.png', '../report/images/results/pedestrian_zone_heatmap_70.png', '../report/images/results/sighting_point_heatmap_500.png', '../report/images/results/driving_prohibited_heatmap_70.png', '../report/images/greenery/combined_heatmap_smoothed_4_to_1.png']
#OVERLAY_RESULT = '../report/images/greenery/combined.png'
#COMBINED_HEATMAP = '../report/images/greenery/combined_heatmap.png'
#TO_OVERLAY = ['../report/images/greenery/forest.jpeg','../report/images/greenery/areas.jpeg']

def compute_heatmap(intensity_finder_obj, long_left, long_right, lat_top, lat_bot, image, result_path,  radius, function, influence_type, heatmap_path):

    # Get the size of the image
    width, height = image.size

    # Get the dimensions
    lat = lat_top - lat_bot
    long = long_right - long_left

    # Get the steps to get the corresponding gps position for each pixel
    lat_step = lat/height
    long_step = long/width

    # Load a heatmap of the same dimensions
    heatMap = image.copy()
    pix = heatMap.load()
    
    heatMap2 = image.copy()
    pix2 = heatMap2.load()

    #heatMap.save(result_path)
    
    # Set the values of each pixel
    for i in range(width):
        print (100/width*i, "%")
        for j in range(height):
            if InfluenceType.ALL_POINTS == INFLUENCE_TYPE:
                temp = intensity_finder_obj.get_intensity(Coordinate(lat_top-j*lat_step, long_left+i*long_step), radius, intensity_finder_obj.exponential, influence_type)
                res = int(255 * sum(temp) / (len(temp) if (len(temp) > 0) else 1))
            else :
                res = int(255 * (intensity_finder_obj.get_intensity(Coordinate(lat_top-j*lat_step, long_left+i*long_step), radius, intensity_finder_obj.exponential, influence_type)))
            
            #pix[i,j] = (255, 255-res , 255-res)
            pix[i,j] = (pix[i,j][0], int(pix[i,j][1]-pix[i,j][1]*res/255), int(pix[i,j][2]-pix[i,j][2]*res/255))
            pix2[i,j] = (res, 0, 0)

    # Save the heatmap at corresponding path
    heatMap.save(result_path)
    heatMap2.save(heatmap_path)

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

def get_map(source_path, result_path, radius, function, influence_type, heatmap_path):

    # Use ContourDrawer to get data
    drawer = ContourDrawer()
    drawer.load_data(SOURCE , ',', [2, 1])

    # Initialise Intensity Finder
    finder = IntensityFinder(drawer.get_data())
    #finder = IntensityFinder([Coordinate(47.404802, 8.501339), Coordinate(47.404802, 8.581339)])

    # Get Zurich map and the latitude/longitude bounds
    long_left, long_right, lat_top, lat_bot, image = get_zurich_map()

    # Create Heatmap
    compute_heatmap(finder, long_left, long_right, lat_top, lat_bot, image, RESULT, RADIUS, IntensityFinder.exponential2 , INFLUENCE_TYPE, HEATMAP)

def combine_maps(other_to_overlayy, result_path, combined_heatmap):

    image = Image.open(ZURICH_MAP_LOC)
    result = image
    pix = result.load()
    
    # Get the size of the image
    width, height = image.size
    
    # Ratio in %
    weights = [20,20,20,20,20]
    
    others = [(asarray(Image.open(i)) * (weights[a] / 100)) for a, i in  enumerate(other_to_overlayy)]
    other = others[0]
    for i in range(len(others)):
        if i != 0:
            other = other + others[i]

    scaler = other[..., 0].max()
    other = other * (255/scaler)
    other = Image.fromarray(other.astype('uint8'))
    other.save(combined_heatmap)
    pix2 = other.load()

    # Set the values of each pixel
    for i in range(width):
        print (100/width*i, "%")
        for j in range(height):
            res = pix2[i,j][0]
            #pix[i,j] = (res, 0, 0)
            pix[i,j] = (pix[i,j][0], int(pix[i,j][1]-pix[i,j][1]*res/255), int(pix[i,j][2]-pix[i,j][2]*res/255))


    #result = asarray(image) * 0.4
    #other = other * 0.6

    #result = (result + other).astype('uint8')
    #result = Image.fromarray(result)

    result.save(result_path)

def compute():
    #get_map(SOURCE, RESULT, RADIUS, IntensityFinder.exponential2, INFLUENCE_TYPE, HEATMAP)
    combine_maps(TO_OVERLAY, OVERLAY_RESULT, COMBINED_HEATMAP)

compute()

