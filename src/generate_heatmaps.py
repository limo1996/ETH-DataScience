import os

from contour.ContourDrawer import ContourDrawer, Settings, Coordinate
from contour.ContourGradients import HeatType
from IntensityFinder import IntensityFinder

FOLDER = '../data/prepared/'
OUT_FOLDER = '../report/contour/'
FILES = ['illumination.csv', 'sighting_point.csv', 'pedestrian_zone.csv']
SEPARATORS = [',', ',', ',']
COLUMNS = [[2,1], [2,1], [2,1]]
RADIUS = 1000

def main():
    for i in range(0, len(FILES)):
        drawer = ContourDrawer()
        drawer.load_data(os.path.join(FOLDER, FILES[i]), SEPARATORS[i], COLUMNS[i])
        settings = Settings(Coordinate(47.376197, 8.545886), 40, 13, HeatType.GREEN_TO_EVERYTHING_RED)
        out_file = '{0}.html'.format(FILES[i][:-4])
        drawer.draw_contour_google_map(settings, os.path.join(OUT_FOLDER, out_file))

if __name__ == '__main__':
    main()