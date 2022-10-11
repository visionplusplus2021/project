from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json
import controller.common  as cm

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/server_type/get', methods=['GET','POST'])
def server_type_get():

    
    result = conn.selectData('select * from visionplusplus.vw_server_type_all')
    return result

@app.route('/server_type/get_activate', methods=['GET','POST'])
def server_type_get_activate():

    result = conn.selectData('select * from visionplusplus.vw_server_type_active')
    return result



@app.route('/server_type/store', methods=['POST'])
def server_type_store():


    server_type_name = request.form.get('server_type_name')

    
    dup_result = conn.checkExistingData('visionplusplus."ServerType"', '''"ServerTypeName" = '{0}'  '''.format(server_type_name))

    
    if not(dup_result):


        data = (str(uuid.uuid4()),
                request.form['server_type_name'].strip(),
                request.form['user_id'])

        conn.callSPParam("CALL sp_server_type_ins(%s,%s,%s);" ,data)

        
    return dup_result
    

    

@app.route('/server_type/update', methods=['PUT'])
def server_type_update():

    updateID = str(request.form['object_id'])
    server_type_name = request.form['server_type_name'].strip()
    dup_result = conn.checkExistingData('visionplusplus."ServerType"', '''"ServerTypeName" = '{0}' and "ServerTypeID" != '{1}'  '''.format(server_type_name,updateID))

    if not(dup_result):

        data = (updateID,
                request.form['server_type_name'].strip(),
                request.form['user_id'])

        conn.callSPParam("CALL sp_server_type_upd(%s,%s,%s);" ,data)
        
        
    return dup_result
    



@app.route('/server_type/delete/<val>', methods=['DELETE'])
def server_type_delete(val):

    result = conn.callSP("CALL sp_server_type_del ('{0}' );".format(val))
    return result



@app.route('/server_type/activate/<val>', methods=['POST'])
def server_type_activate(val):

    
    str_data = val.split("_")
    result = conn.callSP("CALL sp_server_type_active ('{0}','{1}' );".format(str_data[0],str_data[1]))
    return result
