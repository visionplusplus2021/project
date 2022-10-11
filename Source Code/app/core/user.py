from datetime import datetime
from flask import Flask, render_template, Response, jsonify, request, redirect, session
from passlib.hash import pbkdf2_sha256
import uuid
from functools import wraps
from flask.helpers import send_file, send_from_directory
from notification import Notification as noti
from core.fire_detection import FireDetection as fire
from core.set_boundary import Set_boundary as set_bd
import time
import os
import cv2
from shapely.geometry import Polygon
import numpy as np
import pandas as pd 
import shutil
import pymongo
from bson import json_util, ObjectId
import json
from flask_cors import CORS

# dbCentral = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(dbCentral)
# dbUser = client.user_login_system
from core.database_connector import ConnectDatabase as DB
import uuid
import datetime

conn = DB()


class User:
    def start_session(self, user):
        #del user[0][2]
        session['logged_in'] = True
        session['user'] = user
        print("======session['user'] ========+> "+str(session['user']))
        return jsonify(user), 200
    
    def signup(self):
        
        
        ##Check Duplicated Data
        user_name = request.form.get('name')
        dup_result = conn.checkExistingData('visionplusplus."User"', '''"UserName" = '{0}'  '''.format(user_name))

        if not(dup_result):
            data = (str(uuid.uuid4()),
                    request.form.get('name'),
                    request.form.get('userType'),
                    pbkdf2_sha256.encrypt(request.form.get('password')),
                    request.form.get('name'),
                    request.form.get('email'),
                    request.form.get('name')
            )
            
            result = conn.callSPParam("CALL sp_user_ins(%s,%s,%s,%s,%s,%s,%s);" ,data)

            if (result):
                    return 'success'
            else:
                return 'fail', 422  
        else:
            return 'Duplicated Data', 44  



    
    def login(self):

        email = request.form.get('email')
        json_data = conn.selectData('''select * from  visionplusplus.vw_user_all where "IsActive" = true and  "UserEmail" = '{0}' '''.format(email))
        user = json.loads(json_data)
    
        if len(user)> 0 :        
            if user and pbkdf2_sha256.verify(request.form.get('password'), user[0][3]):
                return self.start_session(user)
        
        return "Invalid login credentials", 401
    
    def update(self):

        updateID = request.form['object_id']

        


        data = (updateID,
                request.form.get('name'),
                request.form.get('userType'),
                pbkdf2_sha256.encrypt(request.form.get('password')),
                request.form.get('email'),
                "test id"
        )
    

        result = conn.callSPParam("CALL sp_user_upd(%s,%s,%s,%s,%s,%s);" ,data)

        if (result):
                return 'success'
        else:
            return 'fail', 422  



    def delete(self, val):

        result = conn.callSP("CALL sp_user_del('{0}');".format(val))
        return result

    def signout(self):
        session.clear()
        return redirect('/')


    def user_activate(self):
        updateID = request.form['object_id']
        result = conn.callSP("CALL sp_user_active('{0}');".format(updateID))
        return result

    
