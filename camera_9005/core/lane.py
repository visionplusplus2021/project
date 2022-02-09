import cv2

import core.utils as utils
from core.point import Point
from core.line import Line
import time

class Lane(Line):

    # def __init__(self, point1, point2, color, thikness, from_, to_, server):
    #     super().__init__(point1, point2)
        
    #     self.color = color
    #     self.thikness = thikness
    #     self.from_ = from_
    #     self.to_ = to_
    #     self.server = server
    #     self.dict = {'bicycle':0,'car':0,'motorbike':0,'bus':0,'truck':0}
    #     self.totalCount = 0

    def __init__(self, camera_id,boundary_id,lane_name,lane_type,polygon,count):
        
        self.boundary_id = boundary_id
        self.color = ""
        self.polygon =polygon
        self.thikness = 1
        self.lane_name = lane_name
        self.lane_type = lane_type
        self.camera_id = camera_id
        self.count = count
        self.dict = {'bicycle':0,'car':0,'motorbike':0,'bus':0,'truck':0}
        self.totalCount = 0
        self.pre_vehicle = []
        self.new_vehicle = []
        self.update = time.time()
        self.check_no_vehicle = 0

    def draw(self, frame):
        cv2.line(frame, (self.point1.x,self.point1.y), (self.point2.x,self.point2.y), self.color, self.thikness)