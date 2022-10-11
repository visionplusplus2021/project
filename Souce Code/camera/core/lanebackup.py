import cv2

import core.utils as utils
from core.point import Point
from core.line import Line

class Lane(Line):

    unique_ids = []
    instances = []

    def __init__(self, point1, point2, color, thikness, from_, to_):
        super().__init__(point1, point2)
        
        self.color = color
        self.thikness = thikness
        self.from_ = from_
        self.to_ = to_
        self.dict = {'bicycle':0,'car':0,'motorbike':0,'bus':0,'truck':0}
        self.list = []

        Lane.instances.append(self)

    def draw(self, frame):
        cv2.line(frame, (self.point1.x,self.point1.y), (self.point2.x,self.point2.y), self.color, self.thikness)

    def text(self, frame, x, y):
        for key, value in self.dict.items():
            cv2.putText(frame, str(key) + " " + str(value), x, y, 0, 1.5e-3 * frame_height, self.color, 2)
            y += 0.04 * frame_height

    # checks whether the center of a lane falls under a bounding box
    def count_algo1(self, bbox, class_name, object_id):

        index, detected = Detected(bbox)
        if object_id not in self.unique_ids:
            if detected:
                self.unique_ids.append(object_id)
        else: # in unique list
            if not detected:
                self.unique_ids.remove(object_id)


        if bbox[0] <= self.center.x <= bbox[2] and bbox[1] <= self.center.y <= bbox[3]:
            if object_id not in self.combined_list:
                self.combined_list.append(object_id)
                self.dict[class_name] = self.dict[class_name] + 1
            return True
        else:
            if object_id in self.combined_list:
                self.combined_list.remove(object_id)
            return False



    def Detected(self, bbox):
        for i, instance in enumerate(self.instances):
            if bbox[0] <= instance.center.x <= bbox[2] and bbox[1] <= instance.center.y <= bbox[3]:
                return i, True
        return -1, False


    
    # checks whether the center of a bounding box falls under lane bounding box
    def count_algo2(self, bbox, class_name, object_id):
        min_x, max_x = min(self.point1.x,self.point2.x), max(self.point1.x,self.point2.x)
        min_y, max_y = min(self.point1.y,self.point2.y), max(self.point1.y,self.point2.y)

        bbox_center = Point(int((bbox[0]+bbox[2])/2), int((bbox[1]+bbox[3])/2))

        if min_x <= bbox_center.x <= max_x and min_y <= bbox_center.y <= max_y:
            if object_id not in self.list:
                self.list.append(object_id)
                self.dict[class_name] = self.dict[class_name] + 1
            return True
        else:
            if object_id in self.list:
                self.list.remove(object_id)
            return False

    # checks whether the distance from bounding box to lane is smaller than the radius of lane circle
    def count_algo3(self, bbox, class_name, object_id):

        bbox_center = Point(int((bbox[0]+bbox[2])/2), int((bbox[1]+bbox[3])/2))
        bbox_to_lane = Line(bbox_center, self.center)

        if bbox_to_lane.distance <= self.radius:
            if object_id not in self.list:
                self.list.append(object_id)
                self.dict[class_name] = self.dict[class_name] + 1
            return True
        else:
            if object_id in self.list:
                self.list.remove(object_id)
            return False

    
