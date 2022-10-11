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


@app.route('/camera_area/get', methods=['GET','POST'])
def camera_area_get():

    
    result = conn.selectData('select * from visionplusplus.vw_area_all')
    return result

@app.route('/camera_area/getActive', methods=['GET','POST'])
def camera_area_get_active():

    
    result = conn.selectData('select * from visionplusplus.vw_camera_area_active')
    return result


@app.route('/camera_area/getByID/<val>', methods=['GET','POST'])
def camera_area_getByID(val):

    
    result = conn.selectData('''select * from visionplusplus.vw_area_all where "AreaID" = '{0}' '''.format(val))
    return result


@app.route('/camera_area/get_activate', methods=['GET','POST'])
def camera_area_get_activate():
    docs = db["camera_area"].find({"camera_area_activate":"true"})
    json_data = json_util.dumps(docs)
    return json_data


@app.route('/camera_area/store', methods=['POST'])
def camera_area_store():


    
    area_name = request.form.get('area_name')
    dup_result = conn.checkExistingData('visionplusplus."CameraArea"', '''"AreaName" = '{0}'  '''.format(area_name))

    if not(dup_result):


        data = (str(uuid.uuid4()),
                request.form['area_name'].strip(),
                request.form['area_address'].strip(),
                request.form['user_id'].strip())

        dup_result = conn.callSPParam("CALL sp_camera_area_ins(%s,%s,%s,%s);" ,data)
        
        
    return dup_result
    
                            
    
    

@app.route('/camera_area/update', methods=['PUT'])
def camera_area_update():

    updateID = str(request.form['object_id'])
    area_name = request.form.get('area_name')
    dup_result = conn.checkExistingData('visionplusplus."CameraArea"', 
                                        '''"AreaName" = '{0}' and "AreaID" <> '{1}'  '''.format(area_name,updateID))

    if not(dup_result):
        data = (updateID,
                request.form['area_name'].strip(),
                request.form['area_address'].strip(),
                request.form['user_id'].strip()    
            )
        dup_result = conn.callSPParam("CALL sp_camera_area_upd(%s,%s,%s,%s);" ,data)
    return dup_result
    


@app.route('/camera_area/delete/<val>', methods=['DELETE'])
def camera_area_delete(val):

    result = conn.callSP("CALL sp_camera_area_del ('{0}');".format(val))
    return result



@app.route('/camera_area/activate/<id>', methods=['POST'])
def camera_area_activate(id):

    result = conn.callSP("CALL sp_camera_area_active ('{0}');".format(id))
    return result
