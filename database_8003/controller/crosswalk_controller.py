from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json


dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
db = client['city_of_oshawa']

@app.route('/crosswalk/get', methods=['GET','POST'])
def crosswalk_get():
    docs = db["crosswalk"].find()
    json_data = json_util.dumps(docs)
    return json_data

@app.route('/crosswalk/get/<val>', methods=['GET', 'POST'])
def crosswalk_get_by_server(val):
    docs = db["crosswalk"].find({'server': val})
    json_data = json_util.dumps(docs)
    return json_data

@app.route('/crosswalk/store', methods=['POST'])
def crosswalk_store():


    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'server': request.form['crosswalkServer'],
        'crosswalk_name': request.form['crosswalk_name'],
        'camera_id': request.form['camera_id'],
        'camera_name': request.form['camera_name'],
    }
    col = db['crosswalk']
    
    col.insert_one(document).inserted_id
    
    return 'success'

@app.route('/crosswalk/update', methods=['PUT'])
def crosswalk_update():

    updateID = request.form['object_id']

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'server': request.form['crosswalkServer'],
        'name': request.form['crosswalkName'],
    }

    print(document)
    col = db['crosswalk']
    

    if (col.update({'_id': ObjectId(updateID)}, document)):
        return 'success'
    else:
        return 'fail', 422 

@app.route('/crosswalk/delete/<val>', methods=['DELETE'])
def crosswalk_delete(val):

    col = db['crosswalk']
    query = {
        '_id': ObjectId(val)
    }
    print(val)
    col.delete_one(query)
    return 'success'