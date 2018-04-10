from contour.ContourDrawer import ContourDrawer, Settings, Coordinate
from contour.ContourGradients import HeatType

"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np 

x = np.linspace(-3,3,1000)
y = np.linspace(-3,3,1000)

X, Y = np.meshgrid(x,y)
Z = (X**2 + Y**2) / 4
print (Z)

plt.figure()
plt.contourf(X, Y, Z)
plt.show()
"""

def main():
    drawer = ContourDrawer()
    drawer.load_data('../data/prepared/illumination.csv', ',', [2, 1])
    settings = Settings(Coordinate(47.376197, 8.545886), 40, 13, HeatType.GREEN_TO_EVERYTHING_RED)
    drawer.draw_contour_google_map(settings, 'tmp.html')


if __name__ == '__main__':
    main()