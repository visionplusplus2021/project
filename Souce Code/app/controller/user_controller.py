from __main__ import app


from datetime import datetime
from flask import Flask, render_template, Response, jsonify, request, redirect, session
from passlib.hash import pbkdf2_sha256
import uuid
from functools import wraps
from flask.helpers import send_file, send_from_directory
from flask_mysqldb import MySQL
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

from core.user import User


dbCentral = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbCentral)
dbUser = client.user_login_system


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
        if session['user']['userType'] == 'admin':
            return f(*args, **kwargs)
        else: 
            return redirect('/')
    return wrap

@app.route('/user/signup', methods=['POST'])
def userSignup():
    return User().signup()

@app.route('/user/login', methods=['POST'])
def userLogin():
    return User().login()

@app.route('/signout')
def signout():
    session.clear()
    return redirect('/login')