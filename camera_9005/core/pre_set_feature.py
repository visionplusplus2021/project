
import cv2
from shapely.geometry import Point,Polygon
from shapely.geometry import Point as point_shape
import numpy as np
import os
import pandas as pd
from bson import  json_util
import json
import pymongo
from core.general import General

class PreSetFeature:


    gl = General()
    def ___init__(self):
       
       print("")

    def preset_lane_counting(self,id):
        
        dbMain = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
        col = db['counting_boundary']

        
        results = col.find({ "camera_id": id})
        # ObjectId("60f0fe2d451a704bc904eea1")
        #results = col.find_one()


        json_data = json_util.dumps(results)
        j_data = json.loads(json_data)

       
        
        
        return j_data
    
    def preset_area_jaywalking(self,id):
        
        dbMain = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
        col = db['jaywalking_boundary']

        
        results = col.find({ "camera_id": id})
        # ObjectId("60f0fe2d451a704bc904eea1")
        #results = col.find_one()


        json_data = json_util.dumps(results)
        j_data = json.loads(json_data)

       
        
        
        return j_data
    
    def selectAreaTrespassing(self,id,Area):
        gl = General()
        dbMain = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
        col = db['trespassing_boundary']
        results = col.find({ "camera_id": id, }).sort("area_name")
        json_data = json_util.dumps(results)
        j_data = json.loads(json_data)

        
        
        areas = []
        for i in range(len(j_data)):
        
            area = Area(j_data[i]["polygon"],gl.getColorLabel(i), 3, j_data[i]["area_name"], '127.0.0.1:8001')
            area.color = gl.getColorLabel(i)
        
            areas.append(area)
    
        return areas

    def preset_area_trespassing(self,id):
        
        dbMain = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
        col = db['trespassing_boundary']

        
        results = col.find({ "camera_id": id})
        # ObjectId("60f0fe2d451a704bc904eea1")
        #results = col.find_one()


        json_data = json_util.dumps(results)
        j_data = json.loads(json_data)

       
        
        
        return j_data
