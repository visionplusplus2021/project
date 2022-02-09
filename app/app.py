from datetime import datetime
from flask import Flask, render_template, Response, jsonify, request, redirect, session, url_for
from passlib.hash import pbkdf2_sha256
import uuid
from functools import wraps
from flask.helpers import send_file, send_from_directory
from notification import Notification as noti
from core.fire_detection import FireDetection as fire
from core.set_boundary import Set_boundary as set_bd
from controller.set_contact import Set_contact as set_ct
import time
import os
import cv2
from shapely.geometry import Polygon
import numpy as np
import pandas as pd 
import shutil
import pymongo
from bson import  json_util
import json
from flask_cors import CORS
from datetime import timedelta


from core.user import User
# import controller.user_controller

app = Flask(__name__, static_url_path='', static_folder='web/assets', template_folder='web/templates')
app.secret_key = b'\x95s\xb0*/\x16\x95/\x95\xaa\xe8~\x0b\x95HO'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# dbMain = 'mongodb+srv://vision:visionaccess@cluster0.3y6ge.mongodb.net/simcoe_conlin?retryWrites=true&w=majority'
# dbTest = 'mongodb+srv://Soham:password16@vision.dafuj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["VIDEO_UPLOADS"] = "/home/iot-lab/master_vision++/camera/data/video"
app.config["EVENTS"] = "/media/iotlab/Work/master_vision/camera_9005/events/"

bd = set_bd()


dbCentral = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
dbUser = client.user_login_system

from core.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


app.permanent_session_lifetime = timedelta(minutes=5)
user_type = ""
user_id = ""

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else: 
            return redirect('/login')
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['user'][0][2] == 'admin':
            return f(*args, **kwargs)
        else: 
            return redirect('/')
    return wrap

@app.route('/user/signup', methods=['POST'])
def userSignup():
    return User().signup()

@app.route('/user/login', methods=['POST'])
def userLogin():

    user_login  = User().login()

    print("===================session==> "+str(session))
    user_type = session['user'][0][2]
    user_id = session['user'][0][0]
    
    return user_login

@app.route('/user/update', methods=['GET', 'POST'])
def userUpdate():
    return User().update()

@app.route('/user/activate', methods=['GET', 'POST'])
def userActivate():
    
    return User().user_activate()

@app.route('/user/get_byID/<id>', methods=['GET', 'POST'])
def userGetByID(id):



    data=(id)          
    json_data = conn.selectData( '''select * from vw_user_all  where "UserID" = '{0}' '''.format(id))


    print("====User id=====+> "+str(json_data))
    return json_data
    


@app.route('/user/delete/<val>', methods=['GET', 'DELETE'])
def userDelete(val):
    return User().delete(val)



@app.route('/signout')
def signout():
    session.clear()
    return redirect('/login')



@app.route('/login')
def login():
    session.permanent = True
    return render_template('login.html')
    
@app.route('/signup')
def signup():
    return render_template('signup.html')


####################### routes before this line is related to authentication ###########################

database_url = 'http://199.212.33.166:9101'


@app.route('/')
@login_required
def index():

    
    user_type = session['user'][0][2]
    return render_template('index.html', database_url_param=database_url,user_type = user_type,user_id = session['user'][0][0])


@app.route('/video')
@login_required
def video():
    return render_template('video.html', database_url_param=database_url)

@app.route('/demo')
@login_required
def demo():
    return render_template('demo_dashboard.html', database_url_param=database_url)

@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/feature')
@login_required
@admin_required
def feature():
    return render_template('feature.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/camera_stream')
@login_required
@admin_required
def camera_stream():
    return render_template('camera_stream.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/server_type')
@login_required
@admin_required
def server_type():
    return render_template('server_type.html', database_url_param=database_url,user_id = session['user'][0][0])


@app.route('/server')
@login_required
@admin_required
def server():
    return render_template('server.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/lane')
@login_required
@admin_required
def lane():
    return render_template('lane.html', database_url_param=database_url)

@app.route('/crosswalk')
@login_required
@admin_required
def crosswalk():
    return render_template('crosswalk.html', database_url_param=database_url)

@app.route('/vehicle')
@login_required
@admin_required
def vehicle():
    return render_template('vehicle.html', database_url_param=database_url)

@app.route('/pedestrian')
@login_required
@admin_required
def pedestrian():
    return render_template('pedestrian.html', database_url_param=database_url)

@app.route('/camera_group')
@login_required
@admin_required
def camera_group():
    return render_template('camera_group.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/camera_area')
@login_required
@admin_required
def camera_area():
    return render_template('camera_area.html', database_url_param=database_url,user_id = session['user'][0][0])




@app.route('/demo_group')
@login_required
@admin_required
def demo_group():
    return render_template('demo_group.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/customer')
@login_required
@admin_required
def customer():
    return render_template('customer.html', database_url_param=database_url,user_id = session['user'][0][0])

@app.route('/user')
@login_required
@admin_required
def user():
    return render_template('user.html', database_url_param=database_url)


@app.route('/user/get', methods=['GET','POST'])

def user_get():

    json_data = conn.selectData('select * from vw_user_all order by "UserName" ')
    return json_data

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', database_url_param=database_url)

@app.route('/timeseries')
@login_required
def timeseries():
    return render_template('timeseries.html', database_url_param=database_url)

@app.route('/report')
@login_required
def report():
    return render_template('report.html', database_url_param=database_url)

@app.route('/vehicle_report')
@login_required
def vehicle_report():
    return render_template('vehicle_report.html', database_url_param=database_url)

@app.route('/pedestrian_report')
@login_required
def pedestrian_report():
    return render_template('pedestrian_report.html', database_url_param=database_url)

@app.route('/jaywalk_report')
@login_required
def jaywalk_report():
    return render_template('jaywalking_report.html', database_url_param=database_url)

@app.route('/trespassing_report')
@login_required
def trespassing_report():
    return render_template('trespassing_report.html', database_url_param=database_url)



@app.route('/camera_location')
@login_required
def camera_location():
    return render_template('camera_location.html', database_url_param=database_url)

@app.route('/event')
@login_required
def event():
    return render_template('event.html', database_url_param=database_url)

@app.route('/set_boundary/<ip>', methods=['GET', 'POST'])
@login_required
def set_boundary(ip):
    
    img_name = bd.set_boundary(ip)
    return render_template('set_boundary.html', database_url_param=database_url,img_data=img_name,polygon_id= bd.polygon_id,dis_polygon= bd.dis_polygon,ip=ip)


@app.route('/set_jwalk_boundary/<id>', methods=['GET', 'POST'])
@login_required
def set_jwalk_boundary(id):
     
    img_name = bd.set_jwalk_boundary(id)
    return render_template('set_jwalking.html', database_url_param=database_url,img_data=img_name,polygon_id= bd.polygon_id,dis_polygon= bd.dis_polygon,id=id)


@app.route('/set_counting_boundary/<id>', methods=['GET', 'POST'])
@login_required
def set_counting_boundary(id):
    
 
    img_name  = bd.set_counting_boundary(id)
    return render_template('index.html', database_url_param=database_url,img_data=img_name)

@app.route('/set_counting_video_boundary/<id>', methods=['GET', 'POST'])
@login_required
def set_counting_video_boundary(id):
     
    print("===id====+>"+str(id)) 
    img_name,lane_name,lane_type,start_point = bd.set_counting_video_boundary(id)
    return render_template('set_video_counting.html', database_url_param=database_url,img_data=img_name,id=id,lane_name=lane_name,lane_type=lane_type,start_point=start_point)





def loadModel():
    from core.objectdetection import Objectdetection
    objectdetec = Objectdetection(src_weight='./checkpoints/fire-tiny-416')
    return objectdetec


if __name__ == '__main__':
    
    client = pymongo.MongoClient(dbCentral)
    db = client['test']
    documents = db['server']
    doc = documents.find_one({'server_type': 'Application User Interface'})

    print(doc)

    #app.run(host=doc['server_ip'], port=doc['server_port'], debug=True)

    app.run(host='0.0.0.0', port='8000', debug=True)
