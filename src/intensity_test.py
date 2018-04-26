from contour.ContourDrawer import ContourDrawer, Settings, Coordinate
from contour.ContourGradients import HeatType

from IntensityFinder import IntensityFinder, InfluenceType

def main():
    drawer = ContourDrawer()
    drawer.load_data('../data/prepared/sighting_point.csv', ',', [2, 1])
    settings = Settings(Coordinate(47.376197, 8.545886), 40, 13, HeatType.GREEN_TO_EVERYTHING_RED)
    drawer.draw_contour_google_map(settings, 'tmp.html')

    tmp_points = [Coordinate(47.3609189757402, 8.56436224167544),
                  Coordinate(47.3667670374606, 8.53512796728307),
                  Coordinate(47.4236847462579, 8.49993934662773),
                  Coordinate(47.4239788179196, 8.5005708232242)]

    radius = 1000
    for dat in drawer.get_data():
        print (dat.to_string())
    finder = IntensityFinder(drawer.get_data())
    print ("Results: {exponential, exponential2, quadratic, linear}")
    print (finder.get_intensity(tmp_points[0], radius, finder.exponential, InfluenceType.ALL_POINTS))
    print (finder.get_intensity(tmp_points[1], radius, finder.exponential2, InfluenceType.ALL_POINTS))
    print (finder.get_intensity(tmp_points[2], radius, finder.quadratic, InfluenceType.ALL_POINTS))
    print (finder.get_intensity(tmp_points[3], radius, finder.linear, InfluenceType.ALL_POINTS))

if __name__ == '__main__':
    main()