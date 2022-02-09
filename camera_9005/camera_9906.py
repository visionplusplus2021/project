import os
from flask.globals import request
from absl import app, flags, logging
from absl.flags import FLAGS
from flask_cors import CORS,cross_origin
from shapely.geometry import Point,Polygon

from core.camera import Camera
from core.point import Point
from core.lane import Lane
from core.area import Area
from core.crosswalk import Crosswalk
from core.objectdetection import Objectdetection
from core.objectdetection_person import ObjectdetectionPerson
from deep_sort.deepsort import Deepsort
from core.general import General 
from core.pre_set_feature import PreSetFeature 




#from core.cross_det.cross_det import CrossDet

from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort.deepsort import Deepsort
from tools import generate_detections as gdet


import time

from PIL import Image
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


from flask_socketio import SocketIO, emit
from threading import Thread
import sys
from flask import Flask, render_template, Response, jsonify, flash, request, redirect, url_for, send_from_directory

import requests
from datetime import datetime

import json
import csv
import pymongo
from bson import  json_util,ObjectId
from yolo import YOLO
import shutil


ps = PreSetFeature()

COLOR = {'red':(255,0,0),'blue':(0,0,255),'green':(0,255,0),'magneta':(255,0,255),'cyan':(0,255,255),'yellow':(255,255,0)}

point1 = Point(180, 152)
point2 = Point(208,180)
point3 = Point(204,180)
point4 = Point(237,230)
point5 = Point(240,230)
point6 = Point(265,266)
point7 = Point(120,240)
point8 = Point(175,224)

# point1 = Point(288, 252)
# point2 = Point(297,268)
# point3 = Point(304,280)
# point4 = Point(337,338)
# point5 = Point(344,350)
# point6 = Point(370,396)
# point7 = Point(192,360)
# point8 = Point(275,324)

# lane1 = Lane(point1, point2, COLOR['green'], 2, 'simcoe_southbound', 'conlin_westbound', '127.0.0.1:8001')
# lane2 = Lane(point3, point4, COLOR['cyan'], 2, 'simcoe_southbound', 'simcoe_southbound', '127.0.0.1:8001')
# lane3 = Lane(point5, point6, COLOR['yellow'], 2, 'simcoe_southbound', 'conlin_eastbound', '127.0.0.1:8001')
# crosswalk1 = Crosswalk(point7, point8, COLOR['magneta'], 3, 'Crosswalk 1', '127.0.0.1:8001')

lanes = []
crosswalks = []
objectdetec = None
objectdetec_person = None
deeps = None
cdet = None
tracker = None
encoder = None
yolo = None
cap_video =None


gl = General()
gl_port=9905
gl_server = "127.0.0.1"
db_server = "199.212.33.166:9101"
url = gl.getDefaultCamera_byServer(gl_server+":"+str(gl_port))


url = "rtsp://root:Durhamcollege2020@172.21.10.14/axis-media/media.amp?camera=1"

camera = Camera(url, lanes, crosswalks)
camera_name = ""



def loadModel():



    global objectdetec ,objectdetec_person
    global deeps
    global cdet
    global tracker
    global encoder

    print("=========> loading model")
    camera.objectdetec = Objectdetection(src_weight='./checkpoints/yolov4-tiny-vehicle-416')
    camera.objectdetec_person = ObjectdetectionPerson(src_weight='./checkpoints/yolov4-tiny-person-416')

    camera.deeps = Deepsort(model_filename='./model_data/mars-small128.pb')

    print("=========> Starting Thread")
    camera.startGettingRawStream()
    
    


def getImageCountingBoundary(id,dt):
    
    
               
    int_count = -1
    
    #camera.getCameraInformation(id)
    stream = cv2.VideoCapture(camera.stream_address)

    path = '/media/iotlab/Work/master_vision/app/web/assets/img/camera/'
    file_path =os.path.join(path , id+"_"+dt+'.jpg')

    
    for fname in os.listdir(path):
        if fname.startswith(id):
            os.remove(os.path.join(path, fname))


   
    try:
        ret_val, frame = stream.read()
        lanes = camera.selectLane(id)
        print("lanes: "+str(len(lanes)))
        if(len(lanes)>0):
            
            frame = camera.drawLane(frame,lanes)

        isWritten = cv2.imwrite(file_path,frame)
        # path = '/media/iotlab/Work/master_vision/app/web/assets/img/camera'
        # isWritten = cv2.imwrite(os.path.join(path , id+'.jpg'),frame)
    except:
        pass

    # while True:

    #     int_count+=1

    #     if(int_count%30!=0):
            
    #         continue
        
        
    #     ret_val, frame = stream.read()
        
    #     lanes = camera.selectLane(id)

    #     if(len(lanes)>0):
            
    #         frame = camera.drawLane(frame,lanes)
            
    #     frame = cv2.imencode('.jpg', frame)[1].tobytes()
    #     yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    
def yieldRawStream(id):
    
    
    camera.stream_address = camera.getCameraInformation(id)
    stream = cv2.VideoCapture(camera.stream_address)

    while True:
        
          
        ret_val, frame = stream.read()

        
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
       

        


def yieldMainFrame(id):

    
 
    
    out = None
    status = "create"
    int_count = -1
    str_FPS = ""
    
    camera.stream_address = camera.getCameraInformation(id)
    camera.stream = cv2.VideoCapture(camera.stream_address)

    camera.selectLane(id)

    camera.getInitialCounting(id)
    path = '/media/iotlab/Work/master_vision/app/web/assets/img/camera/'
    file_path =os.path.join(path , id+'.jpg')

    while True:
        
          
        frame = camera.getRawFrame()
        #camera.selectLane(id)
        ##### Process
        frame,int_fps = camera.updateProcessedRawStream(frame,id)

        
        
      
                
        
        
        # if not os.path.isfile(file_path):

        if(int_count == 10):
            
            isWritten = cv2.imwrite(file_path,camera.frame)
    
       
        int_count+=1  
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
       
        
        
        
       
        # str_FPS = "FPS: "+str( round(1.0 / (time.time() - start_time),2))
        


        





app = Flask(__name__)
#app.config["EVENTS"] = "events/"
app.config["EVENTS"] = "/media/iotlab/Work/master_vision/camera_9005/events/"
app.config["THUMBNAIL"] = "/media/iotlab/Work/master_vision/app/web/assets/img/stream/"

socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app, resources ={r"/*":{"origins":"*"}})



@app.route('/main_stream/<string:id>')
def main_stream(id):
    
    return Response(yieldMainFrame(id),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream/<string:id>')
def stream(id):
    
    return Response(yieldMainFrame(id),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/jwalking/<string:id>_<int:camera_id>')
def jwalking(id,camera_id):
    
    return Response(yieldMainFrame(id),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_image_counting_byID/<id>', methods=['GET', 'POST'])
def get_image_counting_byID(id):
    
    # a = request.args.get('myid')
    
    # print("==============+> parameter: "+a)
    return Response(getImageCountingBoundary(id,""),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_image_jaywalking_byID/<string:id>', methods=['GET', 'POST'])
def get_image_jaywalking_byID(id):
    
    return Response(getImageJaywalkingBoundary(id),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_image_trespassing_byID/<string:id>', methods=['GET', 'POST'])
def get_image_trespassing_byID(id):
    polygon = None
    try:
        polygon = request.form["polygon"]
    except:
        pass
    return Response(getImageTrespassingBoundary(id,polygon),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/draw_boundary_byID/<string:id>', methods=['GET', 'POST'])
@cross_origin(origin='*')
def draw_boundary_byID(id):
    a = request.args.get('date_time')
    featureType = request.args.get('feature_type')

    
    getImageCountingBoundary(id,a)

    # return jsonify(message="POST request returned")

    message = {'greeting':'success'}
    return "test"


    #return Response(getImageTrespassingBoundary(id,polygon),mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/test_camera_connection/<string:id>', methods=['GET'])
def test_camera_connection(id): 

    print("Create new port")
    try:
        port = int(id)
        file_name =  "camera_"+id+".py"
        shutil.copyfile("camera_7001.py", file_name)
        
    except:
        camera.generateThumbnail(app.config["THUMBNAIL"],id)
    return jsonify(success = True)

@app.route('/run_server_port/<string:id>', methods=['GET'])
def run_server_port(id): 

    import subprocess
    

    print("Create new port")
    file_name =  "camera_"+id+".py"
   

    subprocess.Popen( ["lxterminal", "-e", 'python '+file_name+' '+id ])


    # os.system('python '+file_name+' '+id)
 
    return jsonify(success = True)


@app.route('/update_boundary/<string:id>', methods=['GET'])
def update_boundary(id): 
    print("update_boundary :"+id)
    return Response(getImageCountingBoundary(id,""),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/terminate_processed_thread', methods=['GET'])
def terminate_processed_thread():
    print("=========+++> terminate_processed_thread")
    camera.stream_stopped = True
    camera.processed_stopped = True

    return jsonify(success = True)

@app.route('/activate_processed_thread', methods=['GET'])
def activate_processed_thread():
    
    
    print("=========+++> activate_processed_thread")
    camera.stream_stopped = False
    camera.processed_stopped = False
    camera.startGettingRawStream()
    #camera.startProcessingRawStream()

    return jsonify(success = True)

@socketio.on('control')
def control_check_func(json_data):
    global control_check
    control_check = json_data







@app.route('/getEvents', methods=['GET'])
def eventFetch():
    files = []
    for file in os.listdir("events/"):
        if (file == "jaywalking"):
            for file in os.listdir("events/jaywalking"):
                if file.endswith("avi"):
                    files.append((os.path.join("events/jaywalking/", file)))
                    # print((os.path.join("../camera/events/counting", file)))
        if (file == "accident"):
            for file in os.listdir("events/accident"):
                if file.endswith("avi"):
                    files.append((os.path.join("events/accident/", file)))
   
    return jsonify(files)


@app.route('/event_view/<folder>/<file_name>')
def event_view(folder, file_name):
    print("=================+++ > event_view")
    return Response(eventGen(folder, file_name),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def eventGen(folder, file_name):

    path = app.config["EVENTS"] +  folder + "/" + file_name
    cap = cv2.VideoCapture(path)    

    print(path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        


        if not ret:
            frame = cv2.VideoCapture(path)
            break
        if ret:
            image = cv2.resize(frame, (0, 0), None, 1, 1)  # resize image

        frame_detected = cv2.imencode('.jpg', frame)[1].tobytes()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_detected + b'\r\n')
        time.sleep(0.5)
    
    cap.release()
    


@app.route('/display/<type>/<file>')
def display(type, file):
	return redirect(url_for('static', filename='event/' + type + '/' + file))

@app.route('/test_call')
def test_call():
    print("test ====++>")
    return jsonify(success = True)



if __name__ == '__main__':
    # client = pymongo.MongoClient(dbMain)
    # db = client['test']
    # documents = db['server']
    # doc = documents.find_one({'server_name': 'Camera 1'})

    # print(doc)

    # 127.0.0.1:8001
    
    gl_port = int(sys.argv[1]) 
    loadModel()
    
    
    # socketio.run(app, host=doc['server_ip'], port=doc['server_port'], debug=False)
    socketio.run(app, host='0.0.0.0', port=gl_port, debug=False)












# video_path = './data/video/' + video + '.mp4'
# video_path = 'rtsp://root:Durhamcollege2020@172.21.10.14/axis-media/media.amp?camera=2'
# video_path = 'rtsp://root:Durhamcollege2020@172.21.10.14/axis-media/media.amp?camera=' + str(camera_id)
# video_path = 'rtsp://'+str(username)+':'+str(password)+'@'+str(camera_ip)+'/axis-media/media.amp?camera=' + str(camera_id)