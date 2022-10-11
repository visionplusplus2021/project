import cv2

import core.utils as utils
from core.point import Point
from core.line import Line
import time

class Area(Line):

    # def __init__(self, point1, point2, color, thikness, from_, to_, server):
    #     super().__init__(point1, point2)
        
    #     self.color = color
    #     self.thikness = thikness
    #     self.from_ = from_
    #     self.to_ = to_
    #     self.server = server
    #     self.dict = {'bicycle':0,'car':0,'motorbike':0,'bus':0,'truck':0}
    #     self.totalCount = 0

    def __init__(self, polygon, color, thikness, area_name, camera_id):
        
        self.color = color
        self.polygon =polygon
        self.thikness = thikness
        self.area_name = area_name
        self.camera_id = camera_id
        self.dict = {'person':0}
        self.totalCount = 0
        self.last_update = time.time()
        self.check_no_vehicle = 0

    def draw(self, frame):
        cv2.line(frame, (self.point1.x,self.point1.y), (self.point2.x,self.point2.y), self.color, self.thikness)