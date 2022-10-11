import cv2

import core.utils as utils
from core.point import Point
from core.line import Line

class Crosswalk(Line):

    def __init__(self, point1, point2, color, thikness, name, server):
        super().__init__(point1, point2)
        
        self.color = color
        self.thikness = thikness
        self.name = name
        self.server = server
        self.dict = {'person':0}
        self.totalCount = 0

    def draw(self, frame):
        cv2.line(frame, (self.point1.x,self.point1.y), (self.point2.x,self.point2.y), self.color, self.thikness)
