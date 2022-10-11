import os

from absl import app, flags, logging
from absl.flags import FLAGS


from core.camera import Camera
from core.video import Video
from core.point import Point
from core.lane import Lane
from core.crosswalk import Crosswalk

from PIL import Image
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


from flask_socketio import SocketIO, emit
from threading import Thread
import sys
from flask import Flask, render_template, Response, jsonify

import requests
from datetime import datetime

import json
import csv


COLOR = {'red':(255,0,0),'blue':(0,0,255),'green':(0,255,0),'magneta':(255,0,255),'cyan':(0,255,255),'yellow':(255,255,0)}

# point1 = Point(200, 500)
# point2 = Point(280,500)
point3 = Point(300,500)
point4 = Point(430,500)
point5 = Point(450,500)
point6 = Point(550,500)

# lane1 = Lane(point1, point2, COLOR['green'], 3, 'simcoe_southbound', 'conlin_westbound')
lane2 = Lane(point3, point4, COLOR['cyan'], 3, 'simcoe_southbound', 'simcoe_southbound')
lane3 = Lane(point5, point6, COLOR['yellow'], 3, 'simcoe_southbound', 'conlin_eastbound')
# crosswalk1 = Crosswalk(point7, point8, COLOR['magneta'], 3, 'conlin', 'conlin')

lanes = [lane2, lane3]
crosswalks = []


camera = Video('./data/video/video.mp4', lanes, crosswalks)

def yieldRawFrame():
    while True:
        frame = camera.getRawFrame()
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/stream')
def stream():
    return Response(yieldRawFrame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('control')
def control_check_func(json_data):
    global control_check
    control_check = json_data


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port='8002', debug=False)












# video_path = './data/video/' + video + '.mp4'
# video_path = 'rtsp://root:Durhamcollege2020@172.21.10.14/axis-media/media.amp?camera=2'
# video_path = 'rtsp://root:Durhamcollege2020@172.21.10.14/axis-media/media.amp?camera=' + str(camera_id)
# video_path = 'rtsp://'+str(username)+':'+str(password)+'@'+str(camera_ip)+'/axis-media/media.amp?camera=' + str(camera_id)