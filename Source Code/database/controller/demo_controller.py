from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

cors = CORS(app, resources={r"/*": {"origins": "*"}})


# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()



@app.route('/demo/store', methods=['POST'])
def demo_video_create():

    request_data = request.get_json()

    print("==========+>" + str(request_data))
    demo_name = request_data['camera_name']
    dup_result = conn.checkExistingData('visionplusplus."VideoDemo"', '''"VideoDemoName" = '{0}'  '''.format(demo_name))

    if not(dup_result):

       
        UUID = str(uuid.uuid4())
        data = (request_data['uuid'],
                request_data['camera_group'],
                request_data['camera_stream'],
                request_data['camera_name'],
                request_data['user_id']
                )

        dup_result = conn.callSPParam("CALL sp_video_demo_ins(%s,%s,%s,%s,%s);" ,data)
        
        #### Select 
        
    return dup_result
    
    


@app.route('/demo/update', methods=['PUT'])
def demo_update():
    
    request_data = request.get_json()
    print(request_data)

    #updateID = request_data['object_id']

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'name': request_data['camera_name'],
        'url': request_data['camera_url'],
        'server': request_data['camera_server'],
        'group': request_data['camera_group'],
        # 'latitude': request_data['camera_latitude'],
        # 'longitude': request_data['camera_longitude'],
        'features': request_data['features'],
    }
    print(document)
    documents = db['demo']
    if (documents.update({'name': request_data['camera_name']}, {"$set": document})):
        #checkDefaultCamera(updateID)
        return 'success'
    else:
        return 'fail', 422

@app.route('/demo/setActive', methods=['PUT'])
def demo_set_active():
    
    request_data = request.get_json()
    print(request_data)

    updateID = request_data['object_id']

    documents = db['demo']
    if (documents.update_many({}, {"$set": {"active": False}})):
        if (documents.update({'_id': ObjectId(updateID)}, {"$set": {"active": request_data['active']}})):
            return 'success'
    else:
        return 'fail', 422

@app.route('/video_demo_file/get', methods=['GET'])
def video_demo_file():

    result = conn.selectData('select * from visionplusplus.vw_video_demo_file')
    return result

@app.route('/demo/delete/<val>', methods=['DELETE'])
def demo_delete(val):

    ### select IP camera
    col = db['demo']
    docs = col.find({ '_id': ObjectId(val)})
    json_data = json_util.dumps(docs)
    j_data = json.loads(json_data)

    if(len(j_data)> 0 ):
        print("=====> delete vehicle "+str(len(j_data)))
        col_vehicle = db['vehicle']
        query = {
        'server':j_data[0]["server"]
        }
        col_vehicle.remove(query)

        col_pedestrian = db['pedestrian']
        query = {
        'server':j_data[0]["server"]
        }
        col_pedestrian.delete_one(query)

        print("===============>")
        

    col = db['demo']
    query = {
        '_id': ObjectId(val)
    }
    col.delete_one(query)

    #### Update Server
    
    server = j_data[0]['server'].split(":")
    docs = db["server"].find({"server_ip":server[0],"server_port":server[1]})
    json_data = json_util.dumps(docs)

    if(len(json_data)>0):
        print(json_data)
        

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'server_used': "false"
    }
    print(document)
    documents = db['server']
    if (documents.update({"server_ip":server[0],"server_port":server[1]}, {"$set": document})):
        return 'success'
    else:
        return 'fail', 422

    return 'success'

@app.route('/demo/deleteAll', methods=['DELETE'])
def demo_deleteAll():

    col = db['demo']
    col.remove()
    return 'success'


def checkDefaultCamera(id):
    return 'success'
    # col = db['camera']
    # docs = col.find({"active":True})
    # json_data = json_util.dumps(docs)
    # j_data = json.loads(json_data)
    # if(len(j_data) == 0 ):
        
        


    #     documents = db['camera']
        
    #     if (documents.update({'_id': ObjectId(id)}, {"$set": {"active": True}})):
    #         return 'success'
    #     else:
           # return 'fail', 422

