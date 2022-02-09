from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})







# this is a random line
import controller.camera_group_controller
import controller.camera_area_controller
import controller.camera_stream_controller
import controller.camera_controller


import controller.video_controller
import controller.demo_group_controller
import controller.demo_controller

import controller.feature_controller

import controller.crosswalk_controller
import controller.lane_controller

import controller.server_type_controller
import controller.server_controller
import controller.event_controller
import controller.repot_controller
import controller.boundary_controller
import controller.jwalk_boundary_controller
import controller.customer_controller

import controller.vehicle_controller
import controller.pedestrian_controller
import controller.jaywalk_controller
import controller.trespassing_controller

import controller.set_counting_boundary
import controller.set_jaywalking_boundary
import controller.set_trespassing_boundary
import controller.set_counting_video_boundary
from sqlalchemy import text

dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
db = client['city_of_oshawa']




@app.route("/")
def index():
    noti = conn()
    cursor = noti.connectDatabase()

    print("============+>"+str(cursor))
    cursor.execute('SELECT * FROM visionplusplus."CameraGroup"')
    data = cursor.fetchall()
 
    
    return str(data)


if __name__ == '__main__':

    # client = pymongo.MongoClient(dbTest)
    # db = client['city_of_oshawa']
    # documents = db['server']
    # doc = documents.find_one({'server_type': 'Database'})
 
    #app.run(host=doc['server_ip'], port=doc['server_port'], debug=False)
    app.run(host='0.0.0.0', port='9101', debug=True)
