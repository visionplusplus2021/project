from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json



    

def fn_setActivate(db,table_name,column_name,column_id,id):
    print("fn_setActivate")


    col = db[table_name]
    result = col.find_one({column_id:id})
    json_data = json_util.dumps(result)
    j_data = json.loads(json_data)
    str_activate = "false"
    try:
        if(j_data[column_name]) == "false":
            str_activate = "true"
    except:
        pass
    

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
         column_name: str_activate
    }

    if (col.update({column_id:id}, {"$set": document})):
            return 'success'
    else:
        return 'fail', 422  

def fn_checkDuplicate(db,table_name,where_document):

    
    col = db[table_name]
    result = col.find_one(where_document)
    json_data = json_util.dumps(result)
    j_data = json.loads(json_data)
    print("===============> "+str(j_data ))
    if(j_data == None):
        print("no duplicate data")
        return "success"
    else:
        
        return 'duplicate', 44  


