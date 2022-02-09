import pymongo
from datetime import datetime
from flask import jsonify

from bson import json_util, ObjectId
import json

class Store:
    def __init__(self, connection_string, database):

        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database]

    def insertDocument(self, object_id, class_name, from_, to_):
        object_ = {
            'timestamp': datetime.timestamp(datetime.now()), 
            'id': object_id,
            'class': class_name,
            'from': from_,
            'to': to_
        }
        # simcoe_southbound_to_conlin_westbound
        objects_ = self.db[from_ + '_to_' + to_]
        object_inserted_id = objects_.insert_one(object_).inserted_id

    def getDocument(self, collecition):
        objects_ = self.db[collecition]
        
        cursor = objects_.find()
        # list_cur = list(cursor)
        
        json_data = json_util.dumps(cursor) 


        return json_data


    def parse_json(self, data):
        return json.loads(json_util.dumps(data))

