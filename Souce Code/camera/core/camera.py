# import the necessary packages
from base64 import encode
from threading import Thread
import cv2
import pymongo
from bson import  json_util,ObjectId
import json
import random

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
from shapely.geometry import Point,Polygon

# from detectron2.config import get_cfg
# from detectron2.data import MetadataCatalog
# from detectron2.utils.visualizer import ColorMode, Visualizer




physical_devices = tf.config.experimental.list_physical_devices('GPU')


for i in range(len(physical_devices) ):
    tf.config.experimental.set_memory_growth(physical_devices[i], True)
# if len(physical_devices) > 0:
#     tf.config.experimental.set_memory_growth(physical_devices[0], True)
#     tf.config.experimental.set_memory_growth(physical_devices[1], True)
#     tf.config.experimental.set_memory_growth(physical_devices[2], True)
#     tf.config.experimental.set_memory_growth(physical_devices[3], True)

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
from core.notification import Notification as notification
from core.vehicle_counting import VehicleCounting 
from core.pre_set_feature import PreSetFeature 
#from core.cross_det.cross_det import CrossDet
from core.general import General 

from PIL import Image
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import threading
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.detection_yolo import Detection_YOLO
from deep_sort.tracker import Tracker
from deep_sort.deepsort import Deepsort
from tools import generate_detections as gdet


from flask_socketio import SocketIO, emit

import sys
from flask import Flask, render_template, Response, jsonify

import requests
from datetime import datetime


import json
import csv

from core.keyclipwriter import KeyClipWriter
from core.sort import Sort
from skimage.metrics import structural_similarity as compare_ssim



class Camera:

    def __init__(self, url, lanes, crosswalks):
        # self.stream_address = 'rtsp://'+str(username)+':'+str(password)+'@'+str(ip)+'/axis-media/media.amp?camera=' + str(id)
        #tf.config.run_functions_eagerly(True) 
        
        
        self.stream_address = url

        # 'rtsp://root:Durhamcollege2020@12.52.45.14/axis-media/media.amp?camera=2'

        # came ster 145 .. . 

        self.stream = cv2.VideoCapture(self.stream_address)

        self.database = "http://127.0.0.1:6100"
        (self.grabbed, self.frame) = self.stream.read()
        self.processed_frame = self.frame
        self.tresspassing = False
        self.smoke_detection = False
        self.counting_check = False
        self.deidentification = False
        self.jwalking_count = 0
        self.jwalking_undeteceted = 0
        self.frame_height = 480
        self.frame_width = 640
        self.cam_id_test = ""
        self.lanes = lanes
        self.areas = []
        self.areas_trespassing = []
        self.crosswalks = crosswalks
        self.str_features = [False, False, False, False, False, False, False]
        self.feature_vehicle = False
        self.feature_jaywalking = False
        self.lanes_unique_ids = []
        self.crosswalks_unique_ids = []
        #self.startGettingRawStream()
        # self.startProcessingRawStream()
        self.out =None
        self.out_trespassing =None
        self.ip = '127.0.0.1'
        self.bool_data = False
        self.server = ""
        self._id = ""
        self.camera_name = ""
        self.objectdetec = None
        self.objectdetec_person = None
        self.deeps = None
        self.tracker = None
        self.encoder = None
        self.nms_max_overlap = 0.5
        self.yolo = None
        self.previous_frame = []
        self.count_vehicle = 0
        self.count_jaywalking = 0
        self.previous_jawalking = []
        self.last_update_jawalking = time.time()

        self.count_trespassing = 0
        self.previous_trespassing = []
        self.last_update_trespassing = time.time()


        self.thread = None
        self.exit_event = threading.Event()
        self.stream_stopped = False
        self.processed_stopped = False
        
        self.gl = General()
        self.vc = VehicleCounting()
        self.noti = notification()
        self.temp_record =[]
        self.jaywalking_file_name = ""
        self.export_status = ""
        
        # self.checkNotification()

    def startGettingRawStream(self):
        t = threading.Thread(target=self.updateRawStream, args=())
        t.daemon = True
        t.name = "raw_stream_video"
        t.start()
        return self

    def updateRawStream(self):

        int_count = 0
        while True:
            
            (self.grabbed, self.frame) = self.stream.read()

            if(self._id != ""):

                if(int_count%5 ==0):
                    print("updateRawStream = "+str(self._id))
                    self.processed_frame,ftp =  self.updateProcessedRawStream(self.frame,self._id)
                    int_count = 1
            else:
                print("No ID")
            

            int_count+=1
            if(self.stream_stopped):
                return

    def start_process(self):

        
        while(True):
            frame = self.stream.read()
            print("========="+str(self._id)+"============== Processed"+str(len(frame)))

            time.sleep(1)

    def startProcessingRawStream(self):

        print("==================> start_process")
        thread = threading.Thread(target=self.start_process, args=())
        thread.daemon = True
        thread.name = "start_process"
        thread.start()
        
        # return self

    
    # def checkNotification(self):
    #     threading.Timer(5.0, self.checkNotification).start()
        
        
        

    #     docs = requests.get(self.database+'/customer/get_period')
    #     j_data = json.loads(docs.content) 
        
    #     print(j_data)
    #     email = []
        

    #     str_email = ""

    #     ### add email
    #     for data in j_data:
    #         if(str_email != data[7]):
    #             email.append([data[7],data[9]])
    #             str_email = data[7]
        
    #     ### add email
    #     for e in email:
    #         jay_data = []
    #         for data in j_data:
    #             if(e[0] == data[7]):
    #                 jay_data.append([data[0],data[1]])


    #         if(len(jay_data) > 0):
                
                
    #             try:
    #                 requests.post(self.database+"/customer/update_notification/"+e[1])

    #                 self.noti.send_notification_byemail(e,"my Title ",jay_data,self.database)
    #             except:
    #                 pass

    
    def updateProcessedRawStream(self,frame,id):

        start_time = time.time()
        
        #self.selectLane(id)
        
        

        int_index = 0
        int_fps = 0
        
        try:
            frame,boxes, confidences, classes,class_indexs = self.objectdetec.detect_object(frame)

            if(self.feature_vehicle):
                
                

                
                frame, all_vehicle,lanes= self.vc.vehicle_couting_detection(frame,self.database,self.lanes,boxes,classes,
                                                                    class_indexs,confidences,self.previous_frame,self.deeps)
                self.previous_frame = all_vehicle
                self.lanes = lanes

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if(self.feature_jaywalking):

                # frame,boxes, confidences, classes,class_indexs = self.objectdetec.detect_object(frame)
                frame, all_jaywalking ,start_time ,count_jaywalking,out ,temp_record,lanes,file_name,export_status = Trespassing.Jaywalking_couting_detection(frame,self.database,self.lanes,boxes,classes,confidences,self.previous_jawalking,self.last_update_jawalking,self.count_jaywalking,self.out,self.temp_record,self.jaywalking_file_name,self.export_status)
                self.previous_jawalking = all_jaywalking
                self.last_update_jawalking = start_time
                self.count_jaywalking = count_jaywalking
                self.out = out
                self.temp_record = temp_record
                self.lanes = lanes
                self.jaywalking_file_name = file_name
                self.export_status = export_status
        
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # self.processed_frame
            return frame,int_fps
        except:
            pass
    def getCameraInformation(self,id):
        docs = requests.get(self.database+'/camera/getByID/'+id)
        j_data = json.loads(docs.content) 
        self.stream_address = j_data[0][6]
        
        return j_data[0][6]
       

    def selectLane(self,id):

        lanes_data = self.vc.selectLane(self.database,id)

        #lane1 = Lane(point1, point2, COLOR['green'], 2, 'simcoe_southbound', 'conlin_westbound', '127.0.0.1:8001')
        self.lanes = []
        self.feature_vehicle = False
        self.feature_jaywalking = False
        
        for lane_data in lanes_data:
            polygon = lane_data[8].split(")(")
            xy_polygon = []
            for i in range(len(polygon)):
                data = polygon[i].replace("(","").replace(")","").split(",")
                
                xy_polygon.append([int(data[0]),int(data[1])])
               
            pl = Polygon(xy_polygon)
            
            #boundary_id,lane_name,lane_type,polygon
            lane = Lane(lane_data[0],lane_data[6],lane_data[7],lane_data[9],pl,lanes_data[0][12])
            self.lanes.append(lane)


            #### 

            
            if ((lane_data[9] == "vehicle" or lane_data[9] == "pedestrian") and lane_data[13]):
                self.feature_vehicle = True
            
            if (lane_data[9] == "jaywalking" and  lane_data[13]):
                self.feature_jaywalking = True
                

        
        return self.lanes

    def drawLane(self,frame,lanes):
        int_index = 0
        for lane in lanes:
            frame = self.vc.drawPolygon(frame,lane.polygon,self.gl.getColorLabel(int_index))
            
            int_index+=1
            
        return frame


    def getInitialCounting(self,id):

        lanes_count = self.vc.selectVehicleCounting(self.database,id)
        int_index = 0
        for _lane in lanes_count:
            for lane in self.lanes:
                 
                if(lane.boundary_id == _lane[1]):
                    lane.totalCount = _lane[3]
                    lane.color = self.gl.getColorLabel(int_index)
                    
                    int_index+=1
                    break
        


    def generateThumbnail(self,img_folder,id):
    
        

        if(id == "1"):
            return

        sub_fodler = img_folder.find('video') 

        print("my id: "+id)
        data = id.split("_")
        if(sub_fodler > 0):
            
            stream = cv2.VideoCapture("./data/video/"+data[0]+".mp4")
            file_path =os.path.join(img_folder , data[0]+'.jpg')
        else:
            stream_info = self.vc.selectCamerabyStreamID(self.database,id)
            stream = cv2.VideoCapture(stream_info[0][3])
            file_path =os.path.join(img_folder , id+'.jpg')
        
        

        
        
    
        try:
            ret_val, frame = stream.read()
            isWritten = cv2.imwrite(file_path,frame)
            # path = '/media/iotlab/Work/master_vision/app/web/assets/img/camera'
            # isWritten = cv2.imwrite(os.path.join(path , id+'.jpg'),frame)
        except:
            pass




    def drawPolygon(self,frame,polygon,color):
        return Trespassing.drawPolygon(frame,polygon,color)

        
    def getRawFrame(self):
        
        return self.frame

    def getProcessedFrame(self):
        #self.str_features = self.checkFeature(id)
        
        return self.processed_frame
