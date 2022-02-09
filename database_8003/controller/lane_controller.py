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

@app.route('/lane/get', methods=['GET','POST'])
def lane_get():
    docs = db["lane"].find()
    json_data = json_util.dumps(docs)
    return json_data


@app.route('/lane/get/<val>', methods=['GET', 'POST'])
def lane_get_by_server(val):
    docs = db["lane"].find({'server': val})
    json_data = json_util.dumps(docs)
    return json_data


@app.route('/lane/store', methods=['POST'])
def lane_store():
    
    where_document = {    
            'from': request.form['routeFrom'],
            'to': request.form['routeTo']
        }

    result = cm.fn_checkDuplicate(db,"lane",where_document)
    if result == "success":
        document = {
            'timestamp': datetime.timestamp(datetime.now()),
            'server': request.form['routeServer'].strip(),
            'from': request.form['routeFrom'].strip(),
            'to': request.form['routeTo'].strip(),
            'lane_activate': "true"
        }
        col = db['lane']
        
        col.insert_one(document).inserted_id
        
       
    return result

@app.route('/lane/update', methods=['PUT'])
def lane_update():

    updateID = request.form['object_id']

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'server': request.form['routeServer'].strip(),
        'from': request.form['routeFrom'].strip(),
        'to': request.form['routeTo'].strip()
    }

    print(document)
    col = db['lane']
    

    if (col.update({'_id': ObjectId(updateID)}, {"$set": document})):
        return 'success'
    else:
        return 'fail', 422 

@app.route('/lane/delete/<val>', methods=['DELETE'])
def lane_delete(val):

    col = db['lane']
    query = {
        '_id': ObjectId(val)
    }
    print(val)
    col.delete_one(query)
    return 'success'


@app.route('/lane/activate/<id>', methods=['POST'])
def lane_activate(id):
    return cm.fn_setActivate(db,"lane","lane_activate","_id",ObjectId(id))
    # col = db['lane']

    # print("===========+>"+id)
    # result = col.find_one({'_id': ObjectId(id)})
    # json_data = json_util.dumps(result)
    # j_data = json.loads(json_data)
    # str_activate = "false"
    # try:
    #     if(j_data['lane_activate']) == "false":
    #         str_activate = "true"
    # except:
    #     pass
    

    # document = {
        
    #     'lane_activate': str_activate
    # }

    

    # if (col.update({'_id': ObjectId(id)}, {"$set": document})):
    #         return 'success'
    # else:
    #     return 'fail', 422  