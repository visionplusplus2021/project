import cv2
from math import sqrt

import core.utils as utils
from core.point import Point

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

        self.distance = self.getDistance()
        self.center = self.getCenter()
        self.radius = self.getRadius()

    def getDistance(self):
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        # return sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return int((x1 - x2)**2 + (y1 - y2)**2)

    def getCenter(self):
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        center_x = int((x1+x2)/2)
        center_y = int((y1+y2)/2)
        return Point(center_x, center_y)
    
    def getRadius(self):
        return int(self.distance/4)
