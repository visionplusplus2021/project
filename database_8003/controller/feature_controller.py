from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

import controller.common  as cm


# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']
from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/feature/get', methods=['GET','POST'])
def feature_get():

    result = conn.selectData('select * from vw_feature_all')
    return result


@app.route('/feature/get_isActivate', methods=['GET','POST'])
def feature_get_isActivate():
    result = conn.selectData('select * from vw_feature_active')
    return result
    

@app.route('/feature/get_byID/<val>', methods=['GET'])
def feature_getByID(val):

    result = conn.selectData('''select * from vw_feature_all where "FeatureID" = '{0}' '''.format(val))
    return result

@app.route('/feature/store', methods=['POST'])
def feature_store():

    feature_name = request.form.get('feature_name')
    dup_result = conn.checkExistingData('visionplusplus."Feature"', '''"FeatureName" = '{0}'  '''.format(feature_name))

    if not(dup_result):
        bool_event = True
        if(request.form['feature_event'] == "true"):
            bool_event = False


        data = (str(uuid.uuid4()),
                request.form['feature_name'].strip(),
                bool_event,
                request.form['user_id'])

        result = conn.callSPParam("CALL sp_feature_ins(%s,%s,%s,%s);" ,data)

        
    return dup_result
    



@app.route('/feature/update', methods=['PUT'])
def feature_update():




    updateID = str(request.form['object_id'])

    feature_name = request.form.get('feature_name')
    dup_result = conn.checkExistingData('visionplusplus."Feature"', 
                                        '''"FeatureName" = '{0}' and "FeatureID" <> '{1}'  '''.format(feature_name,updateID))


    
    if not(dup_result):
        bool_event = False
        
        if(request.form['feature_event'] == "false"):
            bool_event = True
        
        data = (updateID,
                request.form['feature_name'].strip(),
                bool_event,
                request.form['user_id'])

        conn.callSPParam("CALL sp_feature_upd(%s,%s,%s,%s);" ,data)
        dup_result = "sucesss"
        
    return dup_result
    

@app.route('/feature/delete/<val>', methods=['DELETE'])
def feature_delete(val):

    result = conn.callSP("CALL sp_feature_del ('{0}' );".format(val))
    return result

@app.route('/feature/activate/<val>', methods=['POST'])
def feature_activate(val):

    str_data = val.split("_")
    result = conn.callSP("CALL sp_feature_activate ('{0}','{1}' );".format(str_data[0],str_data[1]))
    return result



    # col = db['feature']
    # result = col.find_one({'_id': ObjectId(id)})
    # json_data = json_util.dumps(result)
    # j_data = json.loads(json_data)
    # str_activate = "false"
    # try:
    #     if(j_data['feature_activate']) == "false":
    #         str_activate = "true"
    # except:
    #     pass
    

    # document = {
    #     'timestamp': datetime.timestamp(datetime.now()),
    #     'feature_activate': str_activate
    # }

    # if (col.update({'_id': ObjectId(id)}, {"$set": document})):
    #         return 'success'
    # else:
    #     return 'fail', 422  

    
