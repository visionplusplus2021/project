from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json
import controller.common  as cm


dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
db = client['city_of_oshawa']


@app.route('/demo_group/get', methods=['GET','POST'])
def demo_group_get():
    docs = db["demo_group"].find().sort("name")
    json_data = json_util.dumps(docs)
    return json_data

@app.route('/demo_group/get_activate', methods=['GET','POST'])
def demo_group_get_activate():
    docs = db["demo_group"].find({"demo_group_activate":"true"})
    json_data = json_util.dumps(docs)
    return json_data


@app.route('/demo_group/store', methods=['POST'])
def demo_group_store():

    where_document = {    
            'name': request.form['group_name'].strip()
        }

    result = cm.fn_checkDuplicate(db,"demo_group",where_document)
    print("===============>"+str(result))
    if result == "success":


        document = {
            'timestamp': datetime.timestamp(datetime.now()),
            'name': request.form['group_name'].strip(),
            'demo_group_activate': 'true'
        }
        col = db['demo_group']
        
        col.insert_one(document).inserted_id
        
    return result

@app.route('/demo_group/update', methods=['PUT'])
def demo_group_update():

    updateID = request.form['object_id']

    where_document = {    
           'name': request.form['group_name'].strip(),
           "_id": {"$ne": ObjectId(updateID)}
        }

    result = cm.fn_checkDuplicate(db,"demo_group",where_document)
    if result == "success":

        document = {
            'timestamp': datetime.timestamp(datetime.now()),
            'name': request.form['group_name'].strip()
        }

        col = db['demo_group']

        col.update({'_id': ObjectId(updateID)},  {"$set": document})
         
    return result

@app.route('/demo_group/delete/<val>', methods=['DELETE'])
def demo_group_delete(val):

    

    col_camera = db['demo']
    query = {
        'group':val
        }
    col_camera.remove(query)

    col = db['demo_group']
    query = {
        '_id': ObjectId(val)
    }
    print(val)
    col.delete_one(query)
    return 'success'


@app.route('/demo_group/activate/<id>', methods=['POST'])
def demo_group_activate(id):


    result =  cm.fn_setActivate(db,"demo_group","demo_group_activate","_id",ObjectId(id))

    if(result == "success"):
        result =  cm.fn_setActivate(db,"demo","active","group",id)

    return result

    # col = db['camera_group']

    # print("===========+>"+id)
    # result = col.find_one({'_id': ObjectId(id)})
    # json_data = json_util.dumps(result)
    # j_data = json.loads(json_data)
    # str_activate = "false"
    # try:
    #     if(j_data['camera_group_activate']) == "false":
    #         str_activate = "true"
    #     else:
    #         ##### set false to the camera 
    #         col_camera = db['camera']
    #         document_camera = {
    #             "active":"false"
    #         }
    #         col_camera.update({'group': id}, {"$set": document_camera})


    # except:
    #     pass
    

    # document = {
        
    #     'camera_group_activate': str_activate
    # }

    

    # if (col.update({'_id': ObjectId(id)}, {"$set": document})):
    #         return 'success'
    # else:
    #     return 'fail', 422  
