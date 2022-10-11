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


@app.route('/trespassing_count/get', methods = ['GET'])
def trespassing_count_get():

    objects_ = db['trespassing_count']
    cursor = objects_.find()
    json_data = json_util.dumps(cursor)
    return json_data


@app.route('/trespassing_count/store', methods=['POST'])
def trespassing_count_store():

    document = {
        'timestamp': str(datetime.now()),
        'camera_id': request.form['camera_id'],
        'camera_name': request.form['camera_name'],
        'area_name': request.form['area_name']
    }

    documents = db['trespassing_count']
    document_inserted_id = documents.insert_one(document).inserted_id
    
    return 'success'



@app.route('/trespassing_boundary/get_area/<id>', methods=['GET','POST'])
def trespassing_boundary_get_area(id):

    
    docs = db["trespassing_boundary"].find({'camera_id': id}).sort("area_name")
    json_data = json_util.dumps(docs)

    return json_data


@app.route('/trespassing_report/get_by_filter', methods = ['GET', 'POST'])
def trespassing_report_get_by_filter():

    
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    camera_name = request.form['camera_name']
    area_name = request.form['area_name']
    
    # server = request.form['server']
    # from_ = request.form['from']
    # to_ = request.form['to']

    # print(type(start))
    # print(start)
    # print(type(end))
    # print(end)
    

    if(start_date == "" ):
        start_date = "1999-01-01"
    if(end_date == "" ):
        end_date = "9999-12-31"




    if(area_name == "" or area_name == "All Areas"):
        area_name = ""

    if(camera_name == "" or camera_name == "All Cameras"):
        camera_name = ""

    
    documents = db['trespassing_count']

    print("=======+>"+str(start_date))

    document_filtered = documents.find(  {"timestamp":{'$gte': start_date.replace("T"," "), '$lt': end_date.replace("T"," ")},
                                          'camera_name': {'$regex': '.*'+camera_name+'.*'},
                                          'area_name': {'$regex': '.*'+area_name+'.*'}
                                          })
    
    json_data = json_util.dumps(document_filtered)

      
    
    return json_data
