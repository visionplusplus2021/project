from __main__ import app

import pymongo
from bson import  json_util,ObjectId
import json
from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

import controller.common  as cm

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()



# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']

@app.route('/customer/get', methods=['GET','POST'])
def contact_get():
    
    result = conn.selectData('SELECT * FROM visionplusplus.vw_contact_all ')
    return result

@app.route('/customer/getByID/<val>', methods=['GET','POST'])
def contact_getByID(val):
    
    result = conn.selectData(''' SELECT * FROM visionplusplus.vw_contact_all where "ContactID" = '{0}' '''.format(val) )
    return result

@app.route('/customer/store', methods=['POST'])
def contact_store():

    
    request_data = request.get_json()
    print("===============+> "+str(request_data))
    contact_name = request_data['contact_name']
    dup_result = conn.checkExistingData('visionplusplus."Contact"', '''"ContactName" = '{0}'  '''.format(contact_name))
    contact_uuid = str(uuid.uuid4())
    if not(dup_result):


        data = (contact_uuid,
                request_data['contact_name'].strip(),
                request_data['mobile'],
                request_data['email'],
                request_data['user_id'])

        result = conn.callSPParam("CALL sp_contact_ins(%s,%s,%s,%s,%s);" ,data)

        
        return result
    else:
            return 'Duplicated Data', 44
    
    
    ##### Add Email
    for feature in request_data['features_email']:  

        data_email = (str(uuid.uuid4()),
                contact_uuid,
                feature,
                True,
                False,
                datetime.datetime.now())

        result = conn.callSPParam("CALL sp_contact_feature_ins(%s,%s,%s,%s,%s,%s);" ,data_email)


        # str_script = ''' INSERT INTO visionplusplus."ContactFeature"(
        #                     "ContactFeatureID","ContactID", "FeatureID","SendEmail","SendSMS", "CreateDate")
        #                     VALUES (%s, %s, %s,%s, %s,%s);'''

        # data = (str(uuid.uuid4()),
        #         UUID,
        #         feature,
        #         True,
        #         False,
        #         datetime.datetime.now())

        # result = conn.insertData(str_script,data)
            
    ##### Add SMS
    for feature in request_data['features_sms']:
        data = (feature,UUID)
        dup_result = conn.checkExistingData('visionplusplus."ContactFeature"', 
                                            '"FeatureID" = %s and "ContactID" =%s ',data)

        ### Insert data

        
        if len(dup_result) == 0:
            
            data_sms = (str(uuid.uuid4()),
                contact_uuid,
                feature,
                False,
                True,
                datetime.datetime.now())

            result = conn.callSPParam("CALL sp_contact_feature_ins(%s,%s,%s,%s,%s,%s);" ,data_sms)


            # str_script = ''' INSERT INTO visionplusplus."ContactFeature"(
            #                  "ContactFeatureID","ContactID", "FeatureID","SendEmail","SendSMS", "CreateDate")
            #                  VALUES (%s, %s, %s,%s, %s,%s);'''

            # data = (str(uuid.uuid4()),
            #         UUID,
            #         feature,
            #         False,
            #         True,
            #         datetime.datetime.now())

            # result = conn.insertData(str_script,data)
        else:
            

            data_sms = (feature,
                        True)

            result = conn.callSPParam("CALL sp_contact_feature_sms_upd(%s,%s);" ,data_sms)



            # bool_sms = True
            # str_script = ''' Update visionplusplus."ContactFeature" set
            #                 "SendSMS" = %s, 
            #                 "UpdateDate" = %s 
            #             where "ContactID" = %s'''

            # data = (bool_sms, 
            #         datetime.datetime.now(), 
            #         UUID)

            # result = conn.updateData(str_script,data)
      
    return result



@app.route('/customer/update', methods=['POST'])
def customer_update():

    request_data = request.get_json()

    print(request_data)
    updateID = str(request_data['object_id'])

    str_script = ''' Update visionplusplus."Contact" set
                            "ContactName" = %s,
                            "ContactEmail" = %s, 
                            "ContactMobile" = %s, 
                            "UpdateDate" = %s 
                        where "ContactID" = %s'''

    data = (request_data['contact_name'].strip(), 
            request_data['email'].strip(), 
            request_data['mobile'].strip(), 
            datetime.datetime.now(), 
            updateID)

    result = conn.updateData(str_script,data)


    ##### Insert Event's Notification

    


    for feature in request_data['features_email']:
        data = (feature,updateID)
        dup_result = conn.checkExistingData('visionplusplus."ContactFeature"', 
                                            '"FeatureID" = %s and "ContactID" =%s ',data)

        ### Insert data

        
        if len(dup_result) == 0:
            
            str_script = ''' INSERT INTO visionplusplus."ContactFeature"(
                             "ContactFeatureID","ContactID", "FeatureID","SendEmail","SendSMS", "CreateDate")
                             VALUES (%s, %s, %s,%s, %s,%s);'''

            data = (str(uuid.uuid4()),
                    updateID,
                    feature,
                    True,
                    True,
                    datetime.datetime.now())

            result = conn.insertData(str_script,data)
            
    return result



    # request_data = request.get_json()
        
    # document = {
    #     'timestamp': datetime.timestamp(datetime.now()),
    #     'contact_name': request_data['contact_name'],
    #     'email': request_data['email'],
    #     'mobile': request_data['mobile'],
    #     'features_email': request_data['features_email'],
    #     'features_sms': request_data['features_sms'],

    # }
    # documents = db['contact']

    # documents.update({'_id': ObjectId(request_data['object_id'])}, {"$set": document})

    return 'success'
    

@app.route('/customer/delete/<val>', methods=['DELETE'])
def customer_delete(val):

    str_script = """DELETE FROM visionplusplus."ContactFeature" where "ContactID" = '{0}' """.format(val)
    result = conn.deleteDataByID(str_script)


    str_script = """DELETE FROM visionplusplus."Contact" where "ContactID" = '{0}' """.format(val)
    result = conn.deleteDataByID(str_script)
                            
    return result


@app.route('/customer/get_feature', methods=['GET','POST'])
def contact_get_feature():

    result = conn.selectData('''select A."FeatureID",A."FeatureName",B."ContactFeatureID",B."ContactID",B."SendEmail",B."SendSMS" from visionplusplus."Feature" as A
                                left outer join visionplusplus."ContactFeature" as B
                                    on(A."FeatureID" = B."FeatureID") ''')
    return result


@app.route('/contact/activate/<id>', methods=['POST'])
def contact_activate(id):

    str_script = """ update visionplusplus."Contact" set "IsActive" = not("IsActive") where "ContactID" = '{0}' """.format(id)
    result = conn.activateStatusByID(str_script)
                            
      
    return result

