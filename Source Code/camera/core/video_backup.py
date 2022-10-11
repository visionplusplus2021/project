# import the necessary packages
from threading import Thread
import cv2
import pymongo
from bson import  json_util,ObjectId
import json

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

class Video:

	def __init__(self, path, lanes, crosswalks):
		self.stream_address = path
		self.stream = cv2.VideoCapture(self.stream_address)

		(self.grabbed, self.frame) = self.stream.read()
		self.processed_frame = self.frame

		self.frame_height = self.frame.shape[0]
		self.frame_width = self.frame.shape[1]

		self.lanes = lanes
		self.crosswalks = crosswalks

		self.lanes_unique_ids = []
		self.crosswalks_unique_ids = []
		
		self.tresspassing = False
		self.smoke_detection = False
		self.counting_check = False
		self.deidentification = False
		self.jwalking_count = 0
		self.jwalking_undeteceted = 0
		self.cam_id_test = ""
		self.str_features = [None] * 5
		self.out = cv2.VideoWriter("events/jaywalking/output.avi", -1, 20.0, (640,480))

		# self.startGettingRawStream()
		self.startProcessingRawStream()


	def startGettingRawStream(self):
		t = Thread(target=self.updateRawStream, args=())
		t.daemon = True
		t.start()
		return self

	def updateRawStream(self):
		while True:
			(self.grabbed, self.frame) = self.stream.read()

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

	def checkFeature(self,id):
		
		str_feature = [None] * 5
		if(id == ""):
			return str_feature
		
		dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
		client = pymongo.MongoClient(dbCentral)
		db = client['test']
		col=db['video']
		
		
		results = col.find({ "id": id })
		# ObjectId("60f0fe2d451a704bc904eea1")
		#results = col.find_one()
		
		
		json_data = json_util.dumps(results)
		j_data = json.loads(json_data)
		
		
		#print(j_data)
		str_feature[4] = id
		for i in range(len(j_data)):
			try:
				for j in range(len(j_data[i]["features"])):
					if("Trespassing" in j_data[i]["features"][j]):
						str_feature[0] = True
						

					if("Smoke Detection" in j_data[i]["features"][j]):
						str_feature[1] = True
						

					if("Counting Check" in j_data[i]["features"][j]):
						str_feature[2] = True
						

					if("Deidentification" in j_data[i]["features"][j]):
						str_feature[3] = True
						
					#{'Smoke Detection': True}, {'Trespassing': True}, {'Counting Check': True}, {'Deidentification': True}
			
			except:
				pass

		# print("===========cam_id_test="+id+"   "+str(str_feature))
		# print(j_data)
		return str_feature

	def updateProcessedRawStream(self):
		objectdetec = Objectdetection(src_weight='./checkpoints/yolov4-416')
		deeps = Deepsort(model_filename='./model_data/mars-small128.pb')
		deiden = Deidentification(src_plate_cascade='./data/blur/haarcascade_russian_plate_number.xml', src_face_cascade='./data/blur/haarcascade_frontalface_default.xml')
		
		database_url = 'http://127.0.0.1:8003/object/create'
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
			(self.grabbed, self.frame) = self.stream.read()

			frame = self.frame
			frame, bboxes, scores, names = objectdetec.detect_object(frame)
			str_features = self.str_features

			
			#################### Sittichai
			# Trespassing.person_detection(frame, bboxes, scores, names)
			#################### End Sittichai

			if(str_features[2] ):
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

			#################### Sittichai
			if(str_features[0]):
				frame = Trespassing.person_detection(frame, bboxes, scores, names)


			frame,bool_detected = Trespassing.jwalking_detection(frame, bboxes, scores, names)
			if(bool_detected):
				if(self.jwalking_count <= 0 ):
					self.jwalking_count = 0


				elif(self.jwalking_count==2):
					fourcc = cv2.VideoWriter_fourcc(*'XVID')
					timestamp = datetime.now()
					h, w, c = frame.shape
					out = cv2.VideoWriter("events/jaywalking/"+timestamp.strftime("%Y%m%d-%H%M%S")+".avi",fourcc, 3.0, (w, h))



					#noti.send_SMS("IP Camera:"+str(self.ip),"",timestamp.strftime("%Y%m%d-%H%M%S")+".avi")
			
				elif(self.jwalking_count > 2):
					out.write(frame)
					#out = cv2.VideoWriter("events/jaywalking/"+timestamp.strftime("%Y%m%d-%H%M%S")+".avi", f, 20.0, (640,480))
					
				self.jwalking_count += 1
				
			else:
				if(self.jwalking_count > 0 ):
					self.jwalking_count = -1
					if(out.isOpened()):
						out.release()
						
								
				self.jwalking_count -= 1
				

				


			
			#noti.send_notification_email("","ssukreep@gmail.com","5555")
			#################### End Sittichai

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

	def getRawFrame(self,id):
		self.cam_id_test = id
		return self.frame

	def getProcessedFrame(self,id):
		#self.str_features = self.checkFeature(id)
		self.cam_id_test = id
		return self.processed_frame