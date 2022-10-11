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



@app.route('/camera_stream/get', methods=['GET','POST'])
def camera_stream_get():
    
    result = conn.selectData("select * from visionplusplus.vw_camera_stream_all")
    return result

@app.route('/camera_stream/getByID/<val>', methods=['GET','POST'])
def camera_stream_getByID(val):

    result = conn.selectData('''select * from visionplusplus.vw_camera_stream_all where "CameraStreamID" = '{0}' '''.format(val))
    return result


@app.route('/camera_stream/store', methods=['POST'])
def camera_stream_store():

    
    stream_name = request.form.get('name')
    dup_result = conn.checkExistingData('visionplusplus."CameraStream"', '''"CameraStreamName" = '{0}'  '''.format(stream_name))
    print("======dup_result=======+> "+str(dup_result))
    if not(dup_result):

        
        data = (str(uuid.uuid4()),
                request.form['area_id'],
                request.form['name'].strip(),
                request.form['url'].strip(),
                request.form['latitude'],
                request.form['longitude'],
                request.form['user_id'])

        conn.callSPParam("CALL sp_camera_stream_ins(%s,%s,%s,%s,%s,%s,%s);" ,data)
        dup_result ="success"
        
    return dup_result
    


@app.route('/camera_stream/activate/<val>', methods=['POST'])
def camera_stream_activate(val):

    
    str_data = val.split("_")
    result = conn.callSP("CALL sp_camera_stream_activate ('{0}','{1}' );".format(str_data[0],str_data[1]))
    return result



@app.route('/camera_stream/update', methods=['PUT'])
def camera_stream_update():


    updateID = str(request.form['object_id'])

    stream_name = request.form.get('name')
    dup_result = conn.checkExistingData('visionplusplus."CameraStream"', 
                                        '''"CameraStreamName" = '{0}' and "CameraStreamID" <> '{1}'  '''.format(stream_name,updateID))

    if not(dup_result):
        data = (updateID,
                    request.form['area_id'],
                    request.form['name'].strip(),
                    request.form['url'].strip(),
                    request.form['latitude'],
                    request.form['longitude'],
                    request.form['user_id'])

        conn.callSPParam("CALL sp_camera_stream_upd(%s,%s,%s,%s,%s,%s,%s);" ,data)
        dup_result ="success"
        
    return dup_result
    
@app.route('/camera_stream/delete/<val>', methods=['DELETE'])
def camera_stream_delete(val):

    str_data = val.split("_")
    result = conn.callSP("CALL sp_camera_stream_del ('{0}' );".format(val))
    return result

