import os
# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
# import eventlet
from flask_socketio import SocketIO, emit
from threading import Thread
# eventlet.monkey_patch()
import sys
# FLASK imports
from flask import Flask, render_template, Response, jsonify
import json
import csv
# from core.functions import *

# from flask_cors import CORS

import requests
from requests.auth import HTTPDigestAuth

# tensorflow model using yolov4 weights
weights_path = './checkpoints/yolov4-416'
saved_model_loaded = tf.saved_model.load(weights_path, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']

STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(False,'yolov4')
input_size = 416

# cascade classifiers
plate_cascade = cv2.CascadeClassifier('./data/blur/haarcascade_russian_plate_number.xml')
face_cascade = cv2.CascadeClassifier('./data/blur/haarcascade_frontalface_default.xml')

# socketio global variables
counting_check = True
face_blur_check = True
license_blur_check = True

# Definition of the parameters for deep sort
max_cosine_distance = 0.4
nn_budget = None
nms_max_overlap = 1.0
# initialize deep sort model
model_filename = 'model_data/mars-small128.pb'


def get_video_stream():
    """
        Returns a generator that yields images from the given url. 
        Useful since generators maintain local state. This could also be 
        a class, but at this point in time a generator function is easier.
        Use:
            video_stream = get_video_stream(url, camera_id: Optional[int])
            for image in video_stream:
                ... # Do stuff.
            
            OR 
            while get_video_stream(url, camera_id: Optional[int]):
                ... # Do stuff.
            OR 
            for image in get_video_stream(url, camera_id: Optional[int]):
                ... # Do stuff.
    """
    
    # url = 'http://172.21.10.14/axis-cgi/mjpg/video.cgi?camera=1'
    url = 'http://172.21.10.14/axis-cgi/mjpg/video.cgi'
    camera_id = 1

    url = url + '?' + str(camera_id)
    auth = HTTPDigestAuth('root', 'Durhamcollege2020')

    # GET the video stream
    r = requests.get(url, auth=auth, stream=True)

    # Check if we have access
    if(r.status_code != 200): raise Exception(f'Received unexpected status code {r.status_code}')
    
    # Create byte array
    bytes = bytes()
    
    # Iterate through the chunks (this is an infinite loop until the connection to the stream is stopped)
    for chunk in r.iter_content(chunk_size=1024):
        
        # Add the chunk to the bytes object
        bytes += chunk
        
        # Look for the index of the byte encoding letting us know that a full image has been grabbed.
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        
        # If those bytes exist we reformat the sum of the chunks into a readable image
        if a != -1 and b != -1:
            
            # JPG byte data
            jpg = bytes[a:b+2]
            
            # Trim the byte array of the most recently read JPG image.
            bytes = bytes[b+2:]
            
            # Decode the bytes, i is a proper RGB image.
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            # Show the image
            # cv2.imshow('i', i)
            # if cv2.waitKey(1) == 27:
            #     exit(0)

            # yield the image
            yield i


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def detect_plate(img):
    plate_img = img.copy()
    roi = img.copy()
    plate = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 15) # detects car plates.
    for (x,y,w,h) in plate:
        roi1 = roi[y:y+h, x:x+w, :] # extracting the Region of Interest of license plate for blurring.
        blur = cv2.blur(roi1, ksize=(30,30)) # performing blur operation
        plate_img[y:y+h, x:x+w, :] = blur # replace the original license plate with the blurred one.
        cv2.rectangle(plate_img, (x,y), (x+w, y+h), (51,51,255), 3) # draw rectangles around the edges.
    return plate_img

def detect_face(img):
    face_img = img.copy()
    roi = img.copy()
    plate = face_cascade.detectMultiScale(face_img, scaleFactor = 1.2, minNeighbors = 15) # detects car plates.
    for (x,y,w,h) in plate:
        roi1 = roi[y:y+h, x:x+w, :] # extracting the Region of Interest of face for blurring.
        blur = cv2.blur(roi1, ksize=(30,30)) # performing blur operation
        face_img[y:y+h, x:x+w, :] = blur # replace the original face with the blurred one.
        cv2.rectangle(face_img, (x,y), (x+w, y+h), (51,51,255), 3) # draw rectangles around the edges.
    return face_img


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/video_streaming/<video_name>')
def video_streaming_route(video_name):
    print(video_name)
    return Response(video_streaming(video_name),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_video_stream/')
def get_video_stream_route():
    return Response(get_video_stream(),mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('control')
def control_check_func(json_data):
    global counting_check
    if(json_data['counting_check'] == False):
        counting_check = False
    else:
        counting_check = True
    global face_blur_check
    if(json_data['face_blur_check'] == False):
        face_blur_check = False
    else:
        face_blur_check = True
    global license_blur_check
    if(json_data['license_blur_check'] == False):
        license_blur_check = False
    else:
        license_blur_check = True


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port='5000', debug=False)