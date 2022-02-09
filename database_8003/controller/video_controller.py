from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

import controller.common  as cm


# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/video_demo_file/get', methods=['GET','POST'])
def video_demo_file_get():
    
    result = conn.selectData('''select * from vw_video_demo_file  ''')
    
    print(result)
    return result


@app.route('/video/get', methods=['GET','POST'])
def video_get():
    
    result = conn.selectData('''select * from vw_video_demo_detail_all  ''')
    
    print(result)
    return result

@app.route('/video_demo/getByID/<val>', methods=['GET'])
def video_demo_getByID(val):

    result = conn.selectData('''select * from visionplusplus.vw_video_demo_detail_all where "VideoDemoID" = '{0}' '''.format(val))
    print( "video_demo_getByID   =+++++++++ .> "+str(result))
    return result

@app.route('/video_demo/getFileID/<val>', methods=['GET'])
def video_demo_getFileID(val):

    result = conn.selectData('''select * from vw_video_demo_detail_all  where "VideoDemoFileID" = '{0}' '''.format(val))
    return result


@app.route('/video/getByName/<val>', methods=['GET','POST'])
def video_feature_getByName(val):
    str_data = val.split("_")

    
    result = conn.selectData('''select * from vw_video_demo_detail_all  where "VideoDemoName" = '{0}' '''.format(str_data[0]))

    return result

@app.route('/video_demo_feature/getByID/<val>', methods=['GET','POST'])
def video_demo_feature_getByID(val):

    print("camera_feature_getByID  cameraID: "+val)
    if(val=="1"):
        result = conn.selectData('''select * from vw_camera_feature_add''')
    else:
        result = conn.selectData('''select * from vw_video_demo_feature  where "VideoDemoID" = '{0}' or "VideoDemoFeatureID" is null  '''.format(val))
    return result


@app.route('/video/store', methods=['POST'])
def video_store():


    request_data = request.form

    
    video_name = request_data['video_name']
    dup_result = conn.checkExistingData('visionplusplus."VideoDemoFile"', '''"VideoDemoFileName" = '{0}'  '''.format(video_name))

    if not(dup_result):

        
        data = (
                request_data['uuid'],
                request_data['video_name'],
                request_data['user_id']
                )

        dup_result = conn.callSPParam("CALL sp_video_demo_file_ins (%s,%s,%s);" ,data)
        
        #### Select 
        
    return dup_result


@app.route('/video_demo/delete/<val>', methods=['DELETE'])
def video_demo_delete(val):
    print("=====val========> "+val)
    result = conn.callSP("CALL sp_video_demo_del ('{0}');".format(val))
    return "success"


@app.route('/video_demo_file/delete/<val>', methods=['DELETE'])
def video_demo_file_delete(val):
    print("=====val========> "+val)
    result = conn.callSP("CALL sp_video_demo_file_del ('{0}');".format(val))
    return "success"


@app.route('/video_demo/setActive', methods=['PUT'])
def video_demo_set_active():
    
    request_data = request.get_json()
  
  
    data = (request_data['object_id'],
                request_data['user_id']  
            )
    dup_result = conn.callSPParam("CALL sp_video_demo_active(%s,%s);" ,data)


    return dup_result