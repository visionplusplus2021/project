from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json


dbMain = 'mongodb+srv://vision:visionaccess@cluster0.3y6ge.mongodb.net/simcoe_conlin?retryWrites=true&w=majority'
dbTest = 'mongodb+srv://Soham:password16@vision.dafuj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

############################ routes for report ####################################################
@app.route('/report/get', methods = ['POST'])
def report_get():
    client = pymongo.MongoClient(dbMain)
    db = client['simcoe_conlin']
    request_data = request.get_json()
    collection_name = request_data['from'] + '_to_' + request_data['to']
    print('collection name : ' + collection_name)
    col = db[collection_name]
    # startTimestamp =  float(request_data['startTimestamp'])
    # endTimestamp = float(request_data['endTimestamp'])
    startTimestamp =  float(str(request_data['startTimestamp'])[0:10])
    endTimestamp = float(str(request_data['endTimestamp'])[0:10])
    print(startTimestamp)
    print(endTimestamp)
    docs = col.find({'timestamp' : {'$gt' : startTimestamp, '$lt' : endTimestamp}}).sort("timestamp")
    json_data = json_util.dumps(docs)
    return json_data