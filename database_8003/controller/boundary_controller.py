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

############################ routes for boundry ####################################################
@app.route('/boundary/create', methods=['POST'])
def boundary_create():
    client = pymongo.MongoClient(dbMain)
    # db = client['camera_database']
    db = client['camera_database']
    request_data = request.get_json()
    document = {
        'camera_id': request_data['camera_id'],
        'x_position': request_data['x_position'],
        'y_position': request_data['y_position']
    }
    documents = db['boundary']
    document_inserted_id = documents.insert_one(document).inserted_id
    return 'success'