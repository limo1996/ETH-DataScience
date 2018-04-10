import os
from gmplot import gmplot
from .ContourGradients import getGradient, HeatType

class Coordinate(object):
    """ Class that represents coordinates """
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float):
        """ Creates new instance of Coordinate """
        self.lat = lat
        self.lon = lon

    def from_string(line):
        """ Creates new instance of Coordinate from line in file """
        split = line.split(' ')
        return Coordinate(float(split[0]), float(split[1]))

class Settings(object):
    """ Class that holds settings for contour map drawing """
    center: Coordinate
    radius: int
    zoom: int
    heat_type: HeatType

    # default settings
    def get_default():
        """ Returns default settings """
        return Settings(Coordinate(47.376197, 8.545886), 40, 12, HeatType.GREEN_TO_EVERYTHING_RED)

    def __init__(self, center: Coordinate, radius: int, zoom: int, heat_type: HeatType):
        """ Creates new instance of Settings """
        self.center = center
        self.radius = radius
        self.zoom = zoom
        self.heat_type = heat_type

class ContourDrawer(object):
    def load_data(self, path, separator, columns):
        """ loads data from provided file. """
        with open(path) as file:
            content = file.read()
            content = content.split('\n')
            header = content[0].split('|')
            self.title = header[0]
            content = content[1:]
            self.data = []
            for line in content:
                if not line.isspace() and line:
                    self.data.append(self.parse_line(line, separator, columns))

    def parse_line(self, line, separator, columns):
        split = line.split(separator)
        assert len(columns) == 2
        return Coordinate(float(split[columns[0]]), float(split[columns[1]]))

    def draw_contour_google_map(self, settings: Settings, out_file):
        """ draws provided data on google map with given settings """ 
        latitudes = [i.lat for i in self.data]
        longitudes = [i.lon for i in self.data]

        # creates google map plotter
        plotter = gmplot.GoogleMapPlotter(
            settings.center.lat, 
            settings.center.lon,
            settings.zoom)

        # plots heat map
        plotter.heatmap(
            latitudes,
            longitudes,
            radius=settings.radius,
            gradient=getGradient(settings.heat_type))

        # plot and save to html file
        assert out_file.endswith('.html')
        plotter.draw(out_file)