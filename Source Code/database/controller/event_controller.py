from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

import controller.common  as cm
import socket

dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
db = client['dev']

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/event/get', methods=['GET','POST'])
def event_get():

    
    docs = db["event"].find().sort("timestamp")
    json_data = json_util.dumps(docs)

    return json_data


@app.route('/event/get_by_filter', methods = ['GET', 'POST'])
def event_get_by_filter():

    
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    server = request.form['server']
    event_type = request.form['event_type']
 

    if(start_date == "" ):
        start_date = "1999-01-01"
    if(end_date == "" ):
        end_date = "9999-12-31"

    
    
    documents = db['event']
    start_date = start_date.replace("T"," ")
    end_date = end_date.replace("T"," ")

    str_camera_name = ""
    if(server != "" and  server != "All Cameras"):
        str_camera_name = ''' and  "CameraName" =  '{0}'  '''.format(server)

    str_event_type = ""
    if(event_type != "" and  event_type != "All Type"):
        str_event_type = ''' and  "BoundaryType" =  '{0}'  '''.format(event_type)

        
    #a = datetime.datetime.fromtimestamp(int(start_date)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    start_date = start_date.replace("T"," ")
    end_date = end_date.replace("T"," ")
    
    sql = '''select * from visionplusplus.vw_camera_event  where "timestamp" between '{0}' and '{1}'  {2} {3}
                                   '''.format(start_date,end_date,str_camera_name,str_event_type)

    print(sql)

    result = conn.selectData(sql)

    # result = conn.selectData('''select "ClassName",count(*) from vw_sum_object_counting   where "BoundaryType" = 'pedestrian' and  
    #                             "TimeStamp" between '{0}' and '{1}'  
    #                              {2} group by "ClassName"  '''.format(start_date,end_date,str_lane_name))


    print(str(result))
    return result
    


@app.route('/event/store', methods=['POST'])
def event_store():

    document = {
        'timestamp': str(datetime.now()),
        'event_type': request.form['event_type'],
        'file_name': request.form['file_name'],
        'server': request.form['server'],
        'camera_id': request.form['camera_id'],
        'camera_name': request.form['camera_name']
    }
    col = db['event']
    
    col.insert_one(document).inserted_id
    
    return 'success'

@app.route('/event/update', methods=['PUT'])
def event_update():

    updateID = request.form['object_id']

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'type': request.form['type'],
        'filename': request.form['filename']
    }

    print(document)
    col = db['event']
    col.update({'_id': ObjectId(updateID)}, {"$set": document})
    
    return 'success'

@app.route('/event/delete/<val>', methods=['DELETE'])
def event_delete(val):

    str_script = """DELETE FROM visionplusplus."CameraEvent" where "FileName" = '{0}' """.format(val)
    result = conn.deleteDataByID(str_script)

    str_script = """DELETE FROM visionplusplus."ObjectCounting" where "FileName" = '{0}' """.format(val)
    result = conn.deleteDataByID(str_script)

                            
    return result

# @app.route('/event/delete/<val>', methods=['DELETE'])
# def event_delete(val):

#     col = db['event']
#     query = {
#         '_id': ObjectId(val)
#     }
#     print(val)
#     col.delete_one(query)
#     return 'success'    

