from __main__ import app

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


@app.route('/counting_boundary/store', methods=['POST'])
def counting_boundary_store():

    # ([('camera_id', 'e8b01099-b6a6-45b3-b33e-3a97e0e0c23c'), ('lane_name', 'tets'), ('lane_type', 'vehicle'), ('polygon', '(412,250)(565,215)(586,266)(442,303)')])

    
    boundary_name = request.form['lane_name'].strip()
    camera_feature_id = request.form['camera_feature_id'].strip()

    print("=========+> "+str(request.form))
    
   	# boundary_id character varying,
	# camera_feature_id character varying,
	# boundary_name character varying,
	# boundary_polygon character varying,
	# create_by character varying)

    
    #  'camera_feature__id': feature_id,
    #     'lane_name': laneName,
    #     'lane_type': flexType,
    #     'polygon': polygon


    area_name = request.form.get('area_name')
    dup_result = conn.checkExistingData('visionplusplus."CameraFeatureBoundary"', 
                                        '''"BoundaryName" = '{0}'  and "CameraFeatureID" = '{1}'  '''.format(boundary_name,camera_feature_id))

    if not(dup_result):
        
        
        data = (str(uuid.uuid4()),
                camera_feature_id,
                boundary_name,
                request.form['polygon'].strip(),
                request.form['lane_type'].strip(),
                request.form['user_id'].strip())

        dup_result = conn.callSPParam("CALL sp_camera_feature_boundary_ins(%s,%s,%s,%s,%s,%s);" ,data)
        
        
    return dup_result

@app.route('/camera/getVehicleCountingByCameraID/<val>', methods=['GET'])
def camera_getVehicleCountingByCameraID(val):

    result = conn.selectData('''select * from vw_counting_vehicle  where "CameraID" = '{0}' '''.format(val))
    return result


@app.route('/counting_vehicle/getbyCameraID/<val>', methods=['GET'])
def counting_vehicle_getbyCameraID(val):

    result = conn.selectData('''select * from vw_counting_vehicle  where "CameraID" = '{0}' '''.format(val))
    return result

@app.route('/counting_boundary/get/<val>', methods=['GET','POST'])
def counting_boundary_get(val):
    print("=========+> counting_boundary: "+val)
    result = conn.selectData('''select * from vw_camera_feature_boundary where "CameraFeatureID" = '{0}' '''.format(val))
    return result



@app.route('/counting_boundary/get_lane_vehicle/<val>', methods=['GET','POST'])
def counting_boundary_get_lane_vehicle(val):

    str_data = val.split("_")

    result = conn.selectData('''select * from vw_camera_feature_boundary where "CameraID" = '{0}'  and "BoundaryType" = '{1}' '''.format(str_data[0],str_data[1]))
    return result



@app.route('/counting_boundary/get_lane_pedestrian/<id>', methods=['GET','POST'])
def counting_boundary_get_lane_pedestrian(id):

    print("======counting_boundary_get======>"+id)
    docs = db["counting_boundary"].find({'camera_id': id, "lane_type": "pedestrian"}).sort("lane_name")
    json_data = json_util.dumps(docs)

    return json_data

    

@app.route('/counting_boundary/delete/<val>', methods=['DELETE'])
def counting_boundary_delete(val):
    result = conn.callSP("CALL sp_camera_feature_boundary_del ('{0}');".format(val))
    return result