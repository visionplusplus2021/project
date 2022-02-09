from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json

cors = CORS(app, resources={r"/*": {"origins": "*"}})


# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']


from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()



@app.route('/camera/store', methods=['POST'])
def camera_create():

    request_data = request.get_json()

    print("==========+>" + str(request_data))
    camera_name = request_data['camera_name']
    dup_result = conn.checkExistingData('visionplusplus."Camera"', '''"CameraName" = '{0}'  '''.format(camera_name))

    if not(dup_result):

        server = request_data['camera_server'].split("_")
        UUID = str(uuid.uuid4())
        data = (UUID,
                request_data['camera_group'],
                request_data['camera_stream'],
                server[0],
                request_data['camera_name'],
                request_data['user_id']
                )

        dup_result = conn.callSPParam("CALL sp_camera_ins(%s,%s,%s,%s,%s,%s);" ,data)
        
        #### Select 
        
    return dup_result
      
    


@app.route('/camera/update', methods=['PUT'])
def camera_update():
    request_data = request.get_json()

    print("==Camera Featureupdate==+> "+str(request_data))

    updateID = request_data['object_id']


    camera_name = request_data['camera_name']
    dup_result = conn.checkExistingData('visionplusplus."Camera"', 
                                        '''"CameraName" = '{0}' and "CameraID" <> '{1}'  '''.format(camera_name,updateID))

	# camera_id character varying,
	# camera_group_id character varying,
	# camera_stream_id character varying,
	# server_id character varying,
	# camera_name character varying,
	# update_by character varying)


    if not(dup_result):
        server = request_data['camera_serverID'].split("_")
        print("=========+++++> my server "+server[0])
        data = (updateID,
                request_data['camera_group'].strip(),
                request_data['camera_stream'].strip(),
                server[0],
                request_data['camera_name'].strip(),
                request_data['user_id'].strip()    
            )
        dup_result = conn.callSPParam("CALL sp_camera_upd(%s,%s,%s,%s,%s,%s);" ,data)
  





    ##### Insert Data to Camera Feature
    for feature in request_data['features']:
        
        # camera_feature_id character varying,
        # camera_id character varying,
        # feature_id character varying,
        # update_by character varying)


        print("=============>"+feature)
        data = (updateID,
                feature  
            )
        dup_result = conn.callSPParam("CALL sp_camera_feature_set_active(%s,%s);" ,data)


    return dup_result

    # data=(request_data['camera_name'],
    #       request_data['camera_serverID'])
    # result = conn.selectDataByParam('select * from visionplusplus."Camera" where "CameraName" = %s and "ServerID"= %s',data)
    # j_data = json.loads(result)


    # for feature in request_data['features']:

    #     print("===result==ID ==>"+str(j_data[0][0]))
    #     str_script = ''' INSERT INTO visionplusplus."CameraFeature"(
    #                         "CameraFeatureID", "CameraID", "FeatureID","CreateDate")
    #                         VALUES (%s, %s, %s,%s);'''

    #     data = (str(uuid.uuid4()),
    #             j_data[0][0],
    #             feature,
    #             datetime.datetime.now())

    #     result = conn.insertData(str_script,data)

    return "success"
    


    # request_data = request.get_json()
    # print(request_data)

    # #updateID = request_data['object_id']

    # document = {
    #     'timestamp': datetime.timestamp(datetime.now()),
    #     'name': request_data['camera_name'],
    #     'url': request_data['camera_url'],
    #     'url_name': request_data['camera_url_name'],
    #     'server': request_data['camera_server'],
    #     'group': request_data['camera_group'],
    #     # 'latitude': request_data['camera_latitude'],
    #     # 'longitude': request_data['camera_longitude'],
    #     'features': request_data['features'],
    # }
    # print(document)
    # documents = db['camera']
    # if (documents.update({'name': request_data['camera_name']}, {"$set": document})):
    #     #checkDefaultCamera(updateID)
    #     return 'success'
    # else:
    #     return 'fail', 422

@app.route('/camera_feature/getByID/<val>', methods=['GET','POST'])
def camera_feature_getByID(val):

    print("camera_feature_getByID  cameraID: "+val)
    if(val=="1"):
        result = conn.selectData('''select * from vw_camera_feature_add''')
    else:
        result = conn.selectData('''select * from vw_camera_feature  where "CameraID" = '{0}' or "CameraFeatureID" is null  '''.format(val))
    return result

@app.route('/camera/getByName/<val>', methods=['GET','POST'])
def camera_feature_getByName(val):
    str_data = val.split("_")

    print("===========result getByName=========+ > "+str(str_data[0]))
    result = conn.selectData('''select * from vw_camera_detail_all  where "CameraName" = '{0}' '''.format(str_data[0]))

    print("======result==============+> "+str(result))
    return result



@app.route('/camera/setActive', methods=['PUT'])
def camera_set_active():
    
    request_data = request.get_json()
  
  
    data = (request_data['object_id'],
                request_data['user_id']  
            )
    dup_result = conn.callSPParam("CALL sp_camera_active(%s,%s);" ,data)


    return dup_result


@app.route('/camera/setSuspend', methods=['POST'])
def camera_set_suspend():
    
    

    bool_suspend = False
    
    if( request.form["suspend_status"] == 'false'):
        bool_suspend = True
    
   


    data = (request.form["camera_id"],
            bool_suspend,
            request.form["user_id"]
            )
    dup_result = conn.callSPParam("CALL sp_camera_suspend(%s,%s,%s);" ,data)

    print("=========dup_result=====+++> "+str(dup_result))
    return dup_result


@app.route('/camera/get', methods=['GET'])
def camera_get():

    ## Check set default
    
    conn.callSP("CALL sp_camera_set_default();")
    result = conn.selectData('''select * from visionplusplus.vw_camera_detail_all order by "CameraName" ''')
    return result


@app.route('/camera/getByID/<val>', methods=['GET'])
def camera_getByID(val):

    result = conn.selectData('''select * from visionplusplus.vw_camera_detail_all where "CameraID" = '{0}' '''.format(val))
    return result

@app.route('/camera/getBoundaryByCameraID/<val>', methods=['GET'])
def camera_getBoundaryByID(val):

    result = conn.selectData('''select * from vw_camera_feature_display  where "CameraID" = '{0}' '''.format(val))
    return result

@app.route('/camera/getBoundaryByCameraFeatureID/<val>', methods=['GET'])
def camera_getBoundaryByFeatureID(val):

    result = conn.selectData('''select * from vw_camera_feature_display  where "CameraFeatureID" = '{0}' '''.format(val))
    return result
    
@app.route('/camera/getCamerabyStreamID/<val>', methods=['GET'])
def camera_getCamerabyStreamID(val):

    result = conn.selectData('''select * from vw_camera_stream_active  where "CameraStreamID" = '{0}' '''.format(val))
    return result



@app.route('/camera/delete/<val>', methods=['DELETE'])
def camera_delete(val):
    print("=====val========> "+val)
    result = conn.callSP("CALL sp_camera_del ('{0}');".format(val))
    return "success"
    

@app.route('/camera/deleteAll', methods=['DELETE'])
def camera_deleteAll():

    col = db['camera']
    col.remove()
    return 'success'


def checkDefaultCamera(id):
    return 'success'
    # col = db['camera']
    # docs = col.find({"active":True})
    # json_data = json_util.dumps(docs)
    # j_data = json.loads(json_data)
    # if(len(j_data) == 0 ):
        
        


    #     documents = db['camera']
        
    #     if (documents.update({'_id': ObjectId(id)}, {"$set": {"active": True}})):
    #         return 'success'
    #     else:
           # return 'fail', 422

