from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()

dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
db = client['city_of_oshawa']


@app.route('/pedestrian/store', methods=['POST'])
def pedestrian_store():

    # objects_ = db['pedestrian']
    # cursor = objects_.find({"object_id":request.form['object_id'], 
    #                         "lane_name":request.form['lane_name'],
    #                          })
    # json_data = json_util.dumps(cursor)
    # j_data = json.loads(json_data)

    # if(len(j_data) == 0 ):

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'object_id': request.form['object_id'],
        'class': request.form['class_name'],
        'lane_name': request.form['lane_name'],
        'camera_id': request.form['camera_id'],
        'camera_name': request.form['camera_name']
    }

    documents = db['pedestrian']
    document_inserted_id = documents.insert_one(document).inserted_id
    # else:
    #     print("Duplicate")
    return 'success'

@app.route('/pedestrian/get', methods = ['GET'])
def pedestrian_get():

    objects_ = db['pedestrian']
    cursor = objects_.find()
    json_data = json_util.dumps(cursor)
    return json_data

@app.route('/pedestrian/get_by_filter', methods = ['GET', 'POST'])
def pedestrian_get_by_filter():

    start = float(request.form['start'])/1000.0
    end = float(request.form['end'])/1000.0
    server = request.form['server']
    name = request.form['name']

    # print(type(start))
    # print(start)
    # print(type(end))
    # print(end)

    documents = db['pedestrian']

    # document_filtered = documents.find( {"timestamp":{'$gte': 1630303465.411366, '$lt': 1630306565.411366}, 'server': server, 'from': from_, 'to': to_})

    document_filtered = documents.find( {"timestamp":{'$gte': start, '$lt': end}, 'server': server, 'name': name})
    json_data = json_util.dumps(document_filtered)
    return json_data

@app.route('/pedestian/get_by_filter', methods = ['GET', 'POST'])
def pedestian_get_by_filter():

    start_date = request.form['start_date']
    end_date = request.form['end_date']
    camera_id = request.form['camera_id']
    camera_name = request.form['camera_name']
    area_name = request.form['area_name']
    area_id = request.form['area_id']
    
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
    str_camera_name = ""
    if(area_name != "" and  area_name != "All Areas"):
        str_lane_name = ''' and  "BoundaryID" =  '{0}'  '''.format(area_id)

    if(camera_name != "" and camera_name != "All Cameras"):
        str_camera_name = ''' and  "CameraID" =  '{0}'  '''.format(camera_id)
        

        
    #a = datetime.datetime.fromtimestamp(int(start_date)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    start_date = start_date.replace("T"," ")
    end_date = end_date.replace("T"," ")
    
    sql = '''select "BoundaryName","ClassName", count(*) ,"CameraName"  from vw_sum_object_counting   where "BoundaryType" = 'pedestrian' and  "TimeStamp" between '{0}' and '{1}'  
                                 {2} {3} group by "BoundaryName","ClassName","CameraName"  order by "CameraName" ,"BoundaryName"  '''.format(start_date,end_date,str_lane_name,str_camera_name)
                                
    print(sql)
    result = conn.selectData(sql)
    return result