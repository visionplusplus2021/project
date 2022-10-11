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


@app.route('/camera_group/get', methods=['GET','POST'])
def camera_group_get():

    
    result = conn.selectData('select * from visionplusplus.vw_camera_group_all')
    return result

@app.route('/camera_group/getByID/<val>', methods=['GET','POST'])
def camera_group_getByID(val):

    
    result = conn.selectData('''select * from visionplusplus.vw_camera_group_all where "CameraGroupID" = '{0}' '''.format(val))
    return result


@app.route('/camera_group/get_activate/<val>', methods=['GET','POST'])
def camera_group_get_activate(val):

    result = conn.selectData('''select * from visionplusplus.vw_camera_group_active where "CameraGroupType" = {0} '''.format(val))
    return result



@app.route('/camera_group/store', methods=['POST'])
def camera_group_store():

    group_name = request.form.get('group_name')
    group_type = request.form.get('group_type')

    dup_result = conn.checkExistingData('vw_camera_group_all', 
                                        '''"CameraGroupName" = '{0}'  and  "CameraGroupType" = {1} '''.format(group_name,group_type))


    if not(dup_result):


        data = (str(uuid.uuid4()),
                request.form['group_name'].strip(),
                request.form['group_type'],
                request.form['user_id'])

        dup_result = conn.callSPParam("CALL sp_camera_group_ins(%s,%s,%s,%s);" ,data)
        
        
    return dup_result
     


    

@app.route('/camera_group/update', methods=['PUT'])
def camera_group_update():



    updateID = str(request.form['object_id'])
    group_name = request.form.get('group_name')
    group_type = request.form.get('group_type')

    dup_result = conn.checkExistingData('vw_camera_group_all', 
                                        '''"CameraGroupName" = '{0}' and "CameraGroupID" <> '{1}'  and  "CameraGroupType" = {2} '''.format(group_name,updateID,group_type))

    if not(dup_result):

        data = (updateID,
                    request.form['group_name'].strip(),
                    request.form['group_type'],
                    request.form['user_id'])

        conn.callSPParam("CALL sp_camera_group_upd(%s,%s,%s,%s);" ,data)
        dup_result ="success"
        
    return dup_result


@app.route('/camera_group/delete/<val>', methods=['DELETE'])
def camera_group_delete(val):


   
    result = conn.callSP("CALL sp_camera_group_del ('{0}' );".format(val))

   
    return result[0]




@app.route('/camera_group/activate/<val>', methods=['POST'])
def camera_group_activate(val):


    str_data = val.split("_")
    result = conn.callSP("CALL sp_camera_group_activate ('{0}','{1}' );".format(str_data[0],str_data[1]))
    return result

