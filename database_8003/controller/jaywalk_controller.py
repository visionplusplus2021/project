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

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/jaywalking_count/get', methods = ['GET'])
def jaywalking_count_get():

    objects_ = db['jaywalking_count']
    cursor = objects_.find()
    json_data = json_util.dumps(cursor)
    return json_data


@app.route('/jaywalking_count/store', methods=['POST'])
def jaywalking_count_store():

    document = {
        'timestamp': str(datetime.now()),
        'camera_id': request.form['camera_id'],
        'camera_name': request.form['camera_name'],
        'area_name': request.form['area_name']
    }

    documents = db['jaywalking_count']
    document_inserted_id = documents.insert_one(document).inserted_id
    
    return 'success'



@app.route('/jaywalking_boundary/get_area/<id>', methods=['GET','POST'])
def jaywalking_boundary_get_area(id):

    
    docs = db["jaywalking_boundary"].find({'camera_id': id}).sort("area_name")
    json_data = json_util.dumps(docs)

    return json_data


@app.route('/jaywalking_report/get_by_filter', methods = ['GET', 'POST'])
def jaywalking_report_get_by_filter():

    
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    camera_id = request.form['camera_name']
    lane_name = request.form['area_name']
    
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




    str_lane_name = ""
    if(lane_name != "" and  lane_name != "All Areas"):
        str_lane_name = ''' and  "BoundaryName" =  '{0}'  '''.format(lane_name)

    if(camera_id == "" or camera_id == "All Cameras"):
        camera_id = ""

        
    #a = datetime.datetime.fromtimestamp(int(start_date)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    start_date = start_date.replace("T"," ")
    end_date = end_date.replace("T"," ")
    
    sql = '''select "ClassName",count(*) from vw_sum_object_counting   where "BoundaryType" = 'jaywalking' and  "TimeStamp" between '{0}' and '{1}'  
                                 {2} group by "ClassName"  '''.format(start_date,end_date,str_lane_name)
                                
    print(sql)
    result = conn.selectData(sql)
    return result
