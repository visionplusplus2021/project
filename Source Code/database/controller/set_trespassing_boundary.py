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

@app.route('/trespassing_boundary/store', methods=['POST'])
def trespassing_boundary_store():

    where_document = {    
           'area_name': request.form['area_name'].strip(),
           'camera_id': request.form['camera_id'].strip()
        }

    result = cm.fn_checkDuplicate(db,"trespassing_boundary",where_document)
    if result == "success":

        str_data = request.form['polygon'].split(")(")
        ploygon = []
        for i in range(len(str_data)):
            pre_polygon = str_data[i].replace("(","").replace(")","").split(",")

            X =  int(pre_polygon[0])
            Y =  int(pre_polygon[1])
            ploygon.append([X,Y])
        document = {
            'timestamp': datetime.timestamp(datetime.now()),
            'camera_id': request.form['camera_id'],
            'area_name': request.form['area_name'],
            'polygon': ploygon
        }
        col = db['trespassing_boundary']

       
        col.insert_one(document).inserted_id
    
    return result


@app.route('/trespassing_boundary/get/<id>', methods=['GET','POST'])
def trespassing_boundary_get(id):

   
    docs = db["trespassing_boundary"].find({'camera_id': id}).sort("area_name")
    json_data = json_util.dumps(docs)

    return json_data



@app.route('/trespassing_boundary/delete/<val>', methods=['DELETE'])
def trespassing_boundary_delete(val):
    

   

    ### select IP camera
    col = db['trespassing_boundary']
    docs = col.find({ '_id': ObjectId(val)})
    json_data = json_util.dumps(docs)
    j_data = json.loads(json_data)
    print("====++>"+str(j_data))


    col_trespassing = db['trespassing_count']
    query = {
    'area_name':j_data[0]["area_name"]
    }
    col_trespassing.remove(query)

    print("=========counting_boundary delete===========>"+str(val))
    col = db['trespassing_boundary']
    query = {
        '_id': ObjectId(val)
    }
    
    col.delete_one(query)


    return 'success'
