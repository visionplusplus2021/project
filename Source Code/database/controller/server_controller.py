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

# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/server/get', methods=['GET','POST'])
def server_get():

    result = conn.selectData("select * from visionplusplus.vw_server_all")
    return result


@app.route('/server/get_activate/<val>', methods=['GET','POST'])
def server_get_activate(val):

    
    result = conn.selectData('''select * from visionplusplus.vw_server_active where "IsUsed" = false or "ServerID" = '{0}' '''.format(val))
    return result


    # docs = db["server"].find({"server_activate":"true","server_used":"false"})
    # json_data = json_util.dumps(docs)
    # return json_data


@app.route('/server/store', methods=['POST'])
def server_store():

    server_name = request.form.get('serverName')
    server_IP = request.form['serverIP'].strip()
    server_port = request.form['serverPort'].strip()
    dup_result = conn.checkExistingData('visionplusplus."Server"', '''"ServerName" = '{0}'  or ("ServerIP" = '{1}' and "ServerPort" ='{2}' )  '''.format(server_name,server_IP,server_port))


    if not(dup_result):

        data = (str(uuid.uuid4()),
                request.form['serverType'].strip(),
                request.form['serverName'].strip(),
                request.form['serverIP'].strip(),
                request.form['serverPort'],
                request.form['user_id'].strip())

        dup_result = conn.callSPParam("CALL sp_server_ins(%s,%s,%s,%s,%s,%s);" ,data)
        

     
                            
    return dup_result
  


@app.route('/server/update', methods=['PUT'])
def server_update():

    updateID = request.form['object_id']
    server_name = request.form.get('serverName')
    server_IP = request.form['serverIP'].strip()
    server_port = request.form['serverPort'].strip()
    dup_result = conn.checkExistingData('visionplusplus."Server"', ''' ( "ServerName" = '{0}'  or ("ServerIP" = '{1}' and "ServerPort" ='{2}' ))   
                                        and "ServerID" <> '{3}'    '''.format(server_name,server_IP,server_port,updateID))


    if not(dup_result):
        data = (updateID,
                request.form['serverType'].strip(),
                request.form['serverName'].strip(),
                request.form['serverIP'].strip(),
                request.form['serverPort'],
                request.form['user_id'].strip())

        dup_result = conn.callSPParam("CALL sp_server_upd(%s,%s,%s,%s,%s,%s);" ,data)


    return dup_result



    # where_document = {    
    #        'server_name': request.form['serverName'].strip(),
    #        "_id": {"$ne": ObjectId(updateID)}
    #     }

    # result = cm.fn_checkDuplicate(db,"server",where_document)
    # if result == "success":


    #     document = {
    #         'timestamp': datetime.timestamp(datetime.now()),
    #         'server_name': request.form['serverName'],
    #         'server_ip': request.form['serverIP'],
    #         'server_port': request.form['serverPort'],
    #         'server_type': request.form['serverType']
    #     }

    #     print(document)
    #     col = db['server']
    #     col.update({'_id': ObjectId(updateID)}, {"$set": document})
    
    # return result

@app.route('/server/delete/<val>', methods=['DELETE'])
def server_delete(val):

    str_script = """DELETE FROM visionplusplus."Server" where "ServerID" = '{0}' """.format(val)
    result = conn.deleteDataByID(str_script)
                            
    return result



@app.route('/server/activate/<id>', methods=['POST'])
def server_activate(id):

    str_script = """ update visionplusplus."Server" set "IsActive" = not("IsActive") where "ServerID" = '{0}' """.format(id)
    result = conn.activateStatusByID(str_script)
                            
      
    return result


@app.route('/server/get_available', methods=['GET','POST'])
def server_get_available():
    result = conn.selectData('''SELECT "ServerID", "ServerTypeID", "ServerName", "ServerIP", "ServerPort", "IsActive"
                                    FROM visionplusplus."Server" where "IsActive" = true ''')
    return result

