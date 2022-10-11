# import the necessary packages
from threading import Thread
import cv2

import os
# comment out below line to enable tensorflow logging outputs
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
from math import sqrt
import tensorflow as tf
from tensorflow.python.client import device_lib
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.python.saved_model import tag_constants

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.experimental.set_memory_growth(physical_devices[1], True)
    tf.config.experimental.set_memory_growth(physical_devices[2], True)
    tf.config.experimental.set_memory_growth(physical_devices[3], True)

from absl import app, flags, logging
from absl.flags import FLAGS

import core.utils as utils
from core.yolov4 import filter_boxes
from core.config import cfg

from core.deidentification import Deidentification
from core.objectdetection import Objectdetection
from core.point import Point
from core.lane import Lane
from core.crosswalk import Crosswalk
from core.trespassing import Trespassing

from PIL import Image
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort.deepsort import Deepsort
from tools import generate_detections as gdet

from flask_socketio import SocketIO, emit
from threading import Thread
import sys
from flask import Flask, render_template, Response, jsonify

import requests
from datetime import datetime


import json
import csv

from core.keyclipwriter import KeyClipWriter

class Youtubestream:

	def __init__(self, url):
		self.url = url
		self.stream = cv2.VideoCapture(self.stream_address)

		(self.grabbed, self.frame) = self.stream.read()
		self.processed_frame = self.frame

		self.frame_height = self.frame.shape[0]
		self.frame_width = self.frame.shape[1]

		self.lanes = lanes
		self.crosswalks = crosswalks

		self.lanes_unique_ids = []
		self.crosswalks_unique_ids = []
		
		self.startGettingRawStream()
		self.startProcessingRawStream()

	def startGettingRawStream(self):
		t = Thread(target=self.updateRawStream, args=())
		t.daemon = True
		t.start()
		return self

	def updateRawStream(self):
		while True:
			(self.grabbed, self.frame) = self.stream.read()

	def gen():
    """Video streaming generator function."""
    # url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"
    url = YT_LINK_GLOBAL
    video = pafy.new(url)
    video_new = video.getbest(preftype="mp4")
    camera = cv2.VideoCapture()
    camera.open(video_new.url)
    # cap = cv2.VideoCapture('./data/video/cars.mp4')
    # cap = cv2.VideoCapture(video)
    # print(cap)

    # Read until video is completed
    while(camera.isOpened()):
      # Capture frame-by-frame
        ret, img = camera.read()
        # print(ret)
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            # yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            frame = base64.encodebytes(frame).decode('utf-8')
            # frame = f"data:image/jpeg;base64,{frame}"
            frame = "data:image/jpeg;base64,{}".format(frame)
            yield frame
            # time.sleep(0.03)
        else:
            break

	def startProcessingRawStream(self):
		t = Thread(target=self.updateProcessedRawStream, args=())
		t.daemon = True
		t.start()
		return self

	def crosswalkCounting(self, bbox, class_name, object_id):
		index, detected, counted = -1, False, False
		for i, instance in enumerate(self.crosswalks):
			if bbox[0] <= instance.center.x <= bbox[2] and bbox[1] <= instance.center.y <= bbox[3]:
				index, detected = i, True
				break
		if object_id not in self.crosswalks_unique_ids:
			if detected:
				self.crosswalks_unique_ids.append(object_id)
				self.crosswalks[index].dict[class_name] = self.crosswalks[index].dict[class_name] + 1
				self.crosswalks[index].totalCount = self.crosswalks[index].totalCount + 1
				counted = True
		else: # in unique list
			if not detected:
				self.crosswalks_unique_ids.remove(object_id)
		return counted, index

	def laneCounting(self, bbox, class_name, object_id):
		index, detected, counted = -1, False, False
		for i, instance in enumerate(self.lanes):
			if bbox[0] <= instance.center.x <= bbox[2] and bbox[1] <= instance.center.y <= bbox[3]:
				index, detected = i, True
				break
		if object_id not in self.lanes_unique_ids:
			if detected:
				self.lanes_unique_ids.append(object_id)
				self.lanes[index].dict[class_name] = self.lanes[index].dict[class_name] + 1
				self.lanes[index].totalCount = self.lanes[index].totalCount + 1
				counted = True
		else:
			if not detected:
				self.lanes_unique_ids.remove(object_id)
		return counted, index

	def updateProcessedRawStream(self):
		objectdetec = Objectdetection(src_weight='./checkpoints/yolov4-416')
		deeps = Deepsort(model_filename='./model_data/mars-small128.pb')
		deiden = Deidentification(src_plate_cascade='./data/blur/haarcascade_russian_plate_number.xml', src_face_cascade='./data/blur/haarcascade_frontalface_default.xml')
		
		database_url = 'http://127.0.0.1:8003/create'
		control_check = {'counting_check': True, 'deidentification_check': True}

		config = ConfigProto()
		config.gpu_options.allow_growth = True
		session = InteractiveSession(config=config)

		#####################YOUSSEF
		kcw = KeyClipWriter(bufSize=32)
		global consecFrames
		consecFrames = 1
		#############################

		while True:
			start_time = time.time()
			frame = self.frame
			frame, bboxes, scores, names = objectdetec.detect_object(frame)

			
			#################### Sittichai
			Trespassing.person_detection(frame, bboxes, scores, names)
			#################### End Sittichai

			# camera specific
			for lane in self.lanes:
				lane.draw(frame)
			for crosswalk in self.crosswalks:
				crosswalk.draw(frame)

			tracks = deeps.tracker_tracks(frame, bboxes, scores, names)

			#initialize color map
			cmap = plt.get_cmap('tab20b')
			colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

			###########YOUSSEF
			updateConsecFrames = True
			c = 0
			#################


			# some lines that add another over lay of accident detection bounding boxes
			# frame = accdientDetect(frame)

			if control_check['counting_check']==True:
				# update tracks
				for track in tracks:
					if not track.is_confirmed() or track.time_since_update > 1:
						continue 
					bbox = track.to_tlbr()
					class_name = track.get_class()
					object_id = track.track_id

					# draw bbox on screen
					color = colors[int(object_id) % len(colors)]
					color = [i * 255 for i in color]
					cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
					cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(object_id)))*17, int(bbox[1])), color, -1)
					cv2.putText(frame, class_name + "-" + str(object_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)

					from_, to_ = None, None
					if class_name=='person':
						counted, index = self.crosswalkCounting(bbox, class_name, object_id)
						if counted:
							crosswalk = self.crosswalks[index]
							from_, to_ = crosswalk.from_, crosswalk.to_
					else:
						counted, index = self.laneCounting(bbox, class_name, object_id)
						if counted:
							lane = self.lanes[index]
							from_, to_ = lane.from_, lane.to_
					
					object_ = {
						'object_id': object_id,
						'class_name': class_name,
						'from': from_,
						'to': to_
					}
					requests.post(database_url, data = object_)

					######YOUSSEF
					c+=1
					if c >= 3:
						#save video
						if not kcw.recording:
							timestamp = datetime.now()
							p = "{}/{}.avi".format("events/counting", timestamp.strftime("%Y%m%d-%H%M%S"))
							fourcc = cv2.VideoWriter_fourcc(*'MJPG')
							kcw.start(p, fourcc, 20)
							print("video saved")
						c = 0
					if updateConsecFrames:
						consecFrames += 1
						# update the key frame clip buffer
						kcw.update(frame)
						# if we are recording and reached a threshold on consecutive
						# number of frames with no action, stop recording the clip
					if kcw.recording and consecFrames == 32:
						kcw.finish()
					######################

				frame = self.drawText(frame, 0.05, 0.95, 2, 0.05, True)

			# calculate frames per second of running detections
			fps = 1.0 / (time.time() - start_time)
			# print("FPS: %.2f" % fps)
			frame = np.asarray(frame)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

			if control_check['deidentification_check']==True:
				frame = deiden.detect_plate(frame)
				frame = deiden.detect_face(frame)

			self.processed_frame = frame

	def drawText(self, frame, start_x_ratio, start_y_ratio, text_size, line_space, show_aggregated):
		x = start_x_ratio * self.frame_width
		y = start_y_ratio * self.frame_height
		if show_aggregated:
			for lane in self.lanes:
				cv2.putText(frame, "Total Vehicles: " + str(lane.totalCount), (int(x), int(y)), 0, 1.5e-3 * self.frame_height, lane.color, text_size)
				y -= line_space * self.frame_height
			for crosswalk in self.crosswalks:
				cv2.putText(frame, "Total Pedestrians: " + str(crosswalk.totalCount), (int(x), int(y)), 0, 1.5e-3 * self.frame_height, crosswalk.color, text_size)
				y -= line_space * self.frame_height
		else:
			for lane in self.lanes:
				for key, value in lane.dict.items():
					cv2.putText(frame, str(key) + " " + str(value), (int(x), int(y)), 0, 1.5e-3 * self.frame_height, lane.color, text_size)
					y -= line_space * self.frame_height
			for crosswalk in self.crosswalks:
				for key, value in crosswalk.dict.items():
					cv2.putText(frame, str(key) + " " + str(value), (int(x), int(y)), 0, 1.5e-3 * self.frame_height, crosswalk.color, text_size)
					y -= line_space * self.frame_height
		return frame

	def getRawFrame(self):
		return self.frame

	def getProcessedFrame(self):
		return self.processed_frame