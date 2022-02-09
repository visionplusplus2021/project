from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

import controller.common  as cm


dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
db = client['city_of_oshawa']

@app.route('/counting_video_boundary/get/<id>', methods=['GET','POST'])
def counting_video_boundary_get(id):

    print("======counting_boundary_get======>"+id)
    docs = db["counting_video_boundary"].find({'camera_id': id}).sort("lane_name")
    json_data = json_util.dumps(docs)

    return json_data



@app.route('/counting_video_boundary/get_lane_vehicle/<id>', methods=['GET','POST'])
def counting_video_boundary_get_lane_vehicle(id):

    print("======counting_boundary_get======>"+id)
    docs = db["counting_video_boundary"].find({'camera_id': id, "lane_type": "vehicle"}).sort("lane_name")
    json_data = json_util.dumps(docs)

    return json_data



@app.route('/counting_video_boundary/get_lane_pedestrian/<id>', methods=['GET','POST'])
def counting_video_boundary_get_lane_pedestrian(id):

    print("======counting_boundary_get======>"+id)
    docs = db["counting_video_boundary"].find({'camera_id': id, "lane_type": "pedestrian"}).sort("lane_name")
    json_data = json_util.dumps(docs)

    return json_data

    

@app.route('/counting_video_boundary/delete/<val>', methods=['DELETE'])
def counting_video_boundary_delete(val):
    

   

    ### select IP camera
    col = db['counting_video_boundary']
    docs = col.find({ '_id': ObjectId(val)})
    json_data = json_util.dumps(docs)
    j_data = json.loads(json_data)
    print("====++>"+str(j_data))


    col_vehicle = db['demo']
    query = {
    'lane_name':j_data[0]["lane_name"]
    }
    col_vehicle.remove(query)

    print("=========counting_boundary delete===========>"+str(val))
    col = db['counting_video_boundary']
    query = {
        '_id': ObjectId(val)
    }
    
    col.delete_one(query)


    return 'success'
