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

@app.route('/customer/get_period', methods=['GET','POST'])
def contact_get_period():
    
    result = conn.selectData('SELECT * FROM visionplusplus.vw_notification_period ')
    print("database contact_get_period data: "+ str(result))
    return result


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
                request_data['noti_type'],
                request_data['period_type'],
                request_data['perion_num'],
                request_data['user_id'])

        result = conn.callSPParam("CALL sp_contact_ins(%s,%s,%s,%s,%s,%s,%s,%s);" ,data)

        
       
    else:
            return 'Duplicated Data', 44
    
    
    feature_data =[]

    for feature in request_data['features_email']: 
        feature_data.append([feature,True,False])


    for feature in request_data['features_sms']: 
        bool_check = False
        for f in feature_data: 
            if(f[0]== feature):
                f[2] = True
                bool_check = True
                break

        if(bool_check == False):
            feature_data.append([feature,False,True])

    ##### Add Email
    print("feature_data ====== > "+ str(feature_data))

    for feature in feature_data:  

        
        data_email = (str(uuid.uuid4()),
                contact_uuid,
                feature[0],
                feature[1],
                feature[2],
                request_data['user_id'])

        result = conn.callSPParam("CALL sp_contact_feature_ins(%s,%s,%s,%s,%s,%s);" ,data_email)

        


    # for feature in request_data['features_sms']:
    #     bool_email = False

    #     if()
            
    # ##### Add SMS
    # for feature in request_data['features_sms']:
    #     # data = (feature,UUID)
    #     # dup_result = conn.checkExistingData('visionplusplus."ContactFeature"', 
    #     #                                     '"FeatureID" = %s and "ContactID" =%s ',data)
    #     dup_result = conn.checkExistingData('visionplusplus."ContactFeature"', '''"FeatureID" = '{0}'   and  "ContactID" = '{1}' '''.format(feature,contact_uuid))
    #     ### Insert data

        
    #     if not(dup_result):
            
    #         data_sms = (str(uuid.uuid4()),
    #             contact_uuid,
    #             feature,
    #             False,
    #             True,
    #             request_data['user_id'])

    #         result = conn.callSPParam("CALL sp_contact_feature_ins(%s,%s,%s,%s,%s,%s);" ,data_sms)

    #     else:
    #         print("========my feature========>"+feature)

    #         data_sms = (str(feature))

    #         result = conn.callSPParam("CALL sp_contact_feature_sms_upd(%s);" ,data_sms)
      
    return result


@app.route('/customer/update_notification/<val>', methods=['POST'])
def customer_update_notification(val):

    


    sql = ''' update visionplusplus."Contact"  set "LastNotification" = now()  where "ContactID" = '{0}' '''.format(val)
   
    
    result = conn.deleteDataByID(sql)
    
    



@app.route('/customer/update', methods=['POST'])
def customer_update():

    request_data = request.get_json()

    print("Update Notification ==========+> "+str(request_data))
    contact_uuid = str(request_data['object_id'])


    data = (contact_uuid,
                request_data['contact_name'].strip(),
                request_data['mobile'],
                request_data['email'],
                request_data['user_id'])

    result = conn.callSPParam("CALL sp_contact_upd(%s,%s,%s,%s,%s);" ,data)


    # str_script = ''' Update visionplusplus."Contact" set
    #                         "ContactName" = %s,
    #                         "ContactEmail" = %s, 
    #                         "ContactMobile" = %s, 
    #                         "UpdateDate" = %s 
    #                     where "ContactID" = %s'''

    # data = (request_data['contact_name'].strip(), 
    #         request_data['email'].strip(), 
    #         request_data['mobile'].strip(), 
    #         datetime.datetime.now(), 
    #         contact_uuid)

    # result = conn.updateData(str_script,data)


    ##### Insert Event's Notification

    


    for feature in request_data['features_email']:  

        data_email = (str(uuid.uuid4()),
                contact_uuid,
                feature,
                True,
                False,
                request_data['user_id'])

        result = conn.callSPParam("CALL sp_contact_feature_ins(%s,%s,%s,%s,%s,%s);" ,data_email)

        print("======================= add email: "+feature)

        
            
    ##### Add SMS
    for feature in request_data['features_sms']:
        # data = (feature,UUID)
        # dup_result = conn.checkExistingData('visionplusplus."ContactFeature"', 
        #                                     '"FeatureID" = %s and "ContactID" =%s ',data)
        dup_result = conn.checkExistingData('visionplusplus."ContactFeature"', '''"FeatureID" = '{0}'   and  "ContactID" = '{1}' '''.format(feature,contact_uuid))
        ### Insert data

        print("dup_result :"+str(dup_result)+"  feature:"+feature)
        if not(dup_result):
            
            data_sms = (str(uuid.uuid4()),
                contact_uuid,
                feature,
                False,
                True,
                request_data['user_id'])

            result = conn.callSPParam("CALL sp_contact_feature_ins(%s,%s,%s,%s,%s,%s);" ,data_sms)

        else:
            

            data_sms = (
                feature,
                request_data['user_id'])
            result = conn.callSPParam("CALL sp_contact_feature_sms_upd(%s,%s);" ,data_sms)

            
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
                                    on(A."FeatureID" = B."FeatureID") where a."IsFeature" = false  ''')
    return result


@app.route('/contact/activate/<id>', methods=['POST'])
def contact_activate(id):

    str_script = """ update visionplusplus."Contact" set "IsActive" = not("IsActive") where "ContactID" = '{0}' """.format(id)
    result = conn.activateStatusByID(str_script)
                            
      
    return result

