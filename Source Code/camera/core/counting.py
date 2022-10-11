# import the necessary packages
from threading import Thread
import cv2

class Counting:
    def __init__(self, name="Counting"):

		# initialize the thread name
        self.name = name

    def count_per_lane(self, src):
        min_distance = frame_width
        min_index = 0
        for index, center_point in enumerate(road_center_points):
            # cv2.line(frame, center_point, bbox_center_point, color, 2)
            dis = distance(center_point, bbox_center_point)
            if dis < min_distance:
                min_distance = dis
                min_index = index

        if min_distance < 50: # here 0.5 is threshold
            if object_id not in road_unique_lists[min_index]:
                road_unique_lists[min_index].append(object_id)
                road_dicts[min_index][class_name] = road_dicts[min_index][class_name] + 1
                socketio.emit('object',
                { 
                    'id': object_id,
                    'class': class_name,
                    'from': road_line_from[min_index],
                    'to': road_line_to[min_index]
                }, broadcast = True)
        else:
            if object_id in road_unique_lists[min_index]:
                road_unique_lists[min_index].remove(object_id)

    def count_per_crosswalk(self, src):
        min_distance = frame_width
        min_index = 0
        for index, center_point in enumerate(crossing_center_points):
            # cv2.line(frame, center_point, bbox_center_point, color, 2)
            dis = distance(center_point, bbox_center_point)
            if dis < min_distance:
                min_distance = dis
                min_index = index

        if min_distance < 50: # here 0.5 is threshold
            if object_id not in crossing_unique_lists[min_index]:
                crossing_unique_lists[min_index].append(object_id)
                crossing_dicts[min_index][class_name] = crossing_dicts[min_index][class_name] + 1
                socketio.emit('object',
                { 
                    'id': object_id,
                    'class': class_name,
                    'from': crossing_line_from[min_index],
                    'to': crossing_line_to[min_index]
                }, broadcast = True)
        else:
            if object_id in crossing_unique_lists[min_index]:
                crossing_unique_lists[min_index].remove(object_id)


