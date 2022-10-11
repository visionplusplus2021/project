from __main__ import app

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask import jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId
import json
import datetime

# dbCentral =  "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# db = client['city_of_oshawa']

from controller.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


@app.route('/vehicle_counting/store', methods=['POST'])
def vehicle_counting_store():


    #print("new vehicle: "+str(request.form))
    UUID = str(uuid.uuid4())
    data = (UUID,
            request.form['boundary_id'],
            request.form['class_name'],
            request.form['file_name']
            )

    dup_result = conn.callSPParam("CALL sp_object_counting_ins(%s,%s,%s,%s);" ,data)
       
        #### Select 
        
    return dup_result



    return 'success'

@app.route('/save_event/store', methods=['POST'])
def save_event_store():

    
    UUID = str(uuid.uuid4())
    data = (UUID,
            request.form['boundary_id'],
            request.form['file_name']
            )

    dup_result = conn.callSPParam("CALL sp_camera_event_ins(%s,%s,%s);" ,data)
       
    print("Save Data Event")
    return dup_result



    return 'success'


@app.route('/vehicle/get', methods = ['GET'])
def vehicle_get():

    objects_ = db['vehicle']
    cursor = objects_.find().sort("lane_name")
    json_data = json_util.dumps(cursor)

    return json_data

@app.route('/pedestrian_report/get_by_filter', methods = ['GET', 'POST'])
def pedestrian_report_get_by_filter():

    
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    camera_id = request.form['camera_id']
    lane_name = request.form['lane_name']
    
    # server = request.form['server']
    # from_ = request.form['from']
    # to_ = request.form['to']

    # print(type(start))
    # print(start)
    # print(type(end))
    # print(end)
    
    print("=====camera_id========="+str(camera_id))
    if(start_date == "" ):
        start_date = "1999-01-01"
    if(end_date == "" ):
        end_date = "9999-12-31"


    # print(
    #     datetime.datetime.fromtimestamp(
    #         int(start_date)
    #     ).strftime('%Y-%m-%d %H:%M:%S')
    # )

    str_lane_name = ""
    str_camera = ""
    if(lane_name != "" and  lane_name != "All Lanes"):
        str_lane_name = ''' and  "BoundaryName" =  '{0}'  '''.format(lane_name)

    if(camera_id != "" and camera_id != "All Cameras"):
        str_camera = ''' and  "CameraID" =  '{0}'  '''.format(camera_id)

        
    #a = datetime.datetime.fromtimestamp(int(start_date)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    start_date = start_date.replace("T"," ")
    end_date = end_date.replace("T"," ")
    
    
    #result = conn.selectData('''select * from visionplusplus.vw_sum_object_counting  where "CameraID" = '{0}' '''.format(val))
    result = conn.selectData('''select "ClassName",count(*) from vw_sum_object_counting   where "BoundaryType" = 'pedestrian' and  
                                "TimeStamp" between '{0}' and '{1}'  
                                 {2} {3} group by "ClassName"  '''.format(start_date,end_date,str_camera,str_lane_name))
    
    print(result)
    return result
    
@app.route('/vehicle/get_by_filter', methods = ['GET', 'POST'])
def vehicle_get_by_filter():

    
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    camera_id = request.form['camera_id']
    lane_name = request.form['lane_name']
    
    # server = request.form['server']
    # from_ = request.form['from']
    # to_ = request.form['to']

    # print(type(start))
    # print(start)
    # print(type(end))
    # print(end)
    
    print("=====camera_id========="+str(camera_id))
    if(start_date == "" ):
        start_date = "1999-01-01"
    if(end_date == "" ):
        end_date = "9999-12-31"


    # print(
    #     datetime.datetime.fromtimestamp(
    #         int(start_date)
    #     ).strftime('%Y-%m-%d %H:%M:%S')
    # )

    str_lane_name = ""
    str_camera = ""
    if(lane_name != "" and  lane_name != "All Lanes"):
        str_lane_name = ''' and  "BoundaryName" =  '{0}'  '''.format(lane_name)

    if(camera_id != "" and camera_id != "All Cameras"):
        str_camera = ''' and  "CameraID" =  '{0}'  '''.format(camera_id)


        
    #a = datetime.datetime.fromtimestamp(int(start_date)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    start_date = start_date.replace("T"," ")
    end_date = end_date.replace("T"," ")
    
    sql = '''select "ClassName",count(*) from vw_sum_object_counting   where "BoundaryType" = 'vehicle' and  "TimeStamp" between '{0}' and '{1}'  
                                 {2} {3} group by "ClassName"  '''.format(start_date,end_date,str_camera,str_lane_name)

    print(sql)
    result = conn.selectData(sql)
    return result

    