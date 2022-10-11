
from datetime import datetime
from flask import Flask, render_template, Response, jsonify, request,redirect
from flask.helpers import send_file, send_from_directory
from notification import Notification as noti
from core.fire_detection import FireDetection as fire

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
import certifi
import base64
import requests

from core.general import General

class Set_boundary:
    
    def __init__(self):
        self.ca = certifi.where()
        self.polygon_id = 1
        self.camera_ip = ""
        self.dbMain = 'mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(self.dbMain,tlsCAFile=self.ca)
        self.db = self.client['city_of_oshawa']
        self.dis_polygon = False
        self.img_path = "/home/iotlab/Desktop/teching-city/demo/app/web/assets/img/"
        self.gl = General()
        self.xy_polygon_counting = []
        self.polygon_points = ""

    def drawPolygon(frame,polygon,ploygon_color):
        alpha = 0.2 # that's your transparency factor
        (H, W) = frame.shape[:2]

        xmin = 0
        ymin = 0 
        xmax = int(W / 2)
        ymax = int(H / 2)

        
        int_coords = lambda x: np.array(x).round().astype(np.int32)
        exterior = [int_coords(polygon.exterior.coords)]

        overlay = frame.copy()
        cv2.fillPoly(overlay, exterior, color=ploygon_color)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        return frame

    def set_boundary(self,ip):
        str_ip = ip.split(':')
        #dbMain = 'mongodb+srv://vision:visionaccess@cluster0.3y6ge.mongodb.net/simcoe_conlin?retryWrites=true&w=majority'
        # client = pymongo.MongoClient(self.dbMain)
        # db = client['test']
        if request.method == "POST":
            
            if request.method == "POST":
                if  'submit_button' in request.form: 
                
                    col = self.db['boundary']
                    col.remove()
                    self.get_trespassing_new_id()

                elif 'new_button' in request.form: 
                    self.get_trespassing_new_id()
                elif 'update_button' in request.form: 
                
                    details = request.form
                    try:
                        dis = details['dis_polygon'] 
                        dis = "1"
                        self.dis_polygon = True
                    except:
                        dis = "0"

                    col = self.db['boundary']
                    print("=====dis========="+str(dis))
                    col.update_many({}, {"$set": {"dis_polygon": dis}}) 
                

                else:
                
                
                    
                    details = request.form
                
                    try:
                        dis = details['dis_polygon'] 
                    
                        self.dis_polygon = True
                    except:
                        self.dis_polygon = False

                    document = {
                        'camera_id': str_ip[0],
                        'polygon_id': self.polygon_id,
                        'x_position': details['x'],
                        'y_position': details['y'],
                        'timestamp': datetime.now(),
                        'dis_polygon': self.dis_polygon
                
                    }

  

                    documents = self.db['boundary']
                    document_inserted_id = documents.insert_one(document).inserted_id

            else:
                self.get_trespassing_new_id()


        vidcap = cv2.VideoCapture('http://'+ip+'/stream/1')
        success,frame = vidcap.read()
        
        
        
    
        col = self.db['boundary']
        docs = col.find({"camera_id":str_ip[0]}).sort("timestamp")

        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)
        print(j_data)

        if(len(j_data) > 2 ):
            xy_polygon = []
            polygon_id = int(j_data[0]["polygon_id"])
            self.dis_polygon = int(j_data[0]["dis_polygon"])

            for i in range(len(j_data)):
                
                if(polygon_id != int(j_data[i]["polygon_id"]) and i>0):

                    if(len(xy_polygon)>2):
                        polygon = Polygon(xy_polygon)
                        frame = Set_boundary.drawPolygon(frame,polygon)
                        xy_polygon = []

                x = int(j_data[i]["x_position"])
                y = int(j_data[i]["y_position"])
                xy_polygon.append([x,y])

                polygon_id = int(j_data[i]["polygon_id"])

            try:
                polygon = Polygon(xy_polygon)
                frame = Set_boundary.drawPolygon(frame,polygon)
            except:
                pass
        
        _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
        base64_img = base64.b64encode(encoded_img).decode("utf-8")
        
        return base64_img

    def get_trespassing_new_id(self):
        
        
        
        docs = self.db['boundary'].find().sort('polygon_id', -1 ).limit(1)
        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)
        if(len(j_data) > 0 ):
            self.polygon_id = int(j_data[0]["polygon_id"]) + 1 

        else:
            self.polygon_id =1

    def get_new_id(self):
        
        
        
        docs = self.db['jwalk_boundary'].find().sort('polygon_id', -1 ).limit(1)
        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)
        if(len(j_data) > 0 ):
            self.polygon_id = int(j_data[0]["polygon_id"]) + 1 

        else:
            self.polygon_id =1

    def set_jwalk_boundary(self,id):

        col = self.db['camera']
        docs = col.find({'_id': ObjectId(id)}).sort("timestamp")

        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)

       
        video_ip = ""
        
        
        if(len(j_data)>0):
            video_ip = j_data[0]["url"]
        
        


        if request.method == "POST":

            

            

            if  'submit_button' in request.form: 
                details = request.form
                print("==================="+str(request.form))
                col = self.db['jwalk_boundary']
                
                col.remove({"camera_id": id})
                self.get_new_id()

            elif 'new_button' in request.form: 
                self.get_new_id()
            elif 'update_button' in request.form: 
                
                details = request.form
                try:
                    dis = details['dis_polygon'] 
                    dis = "1"
                    self.dis_polygon = True
                except:
                    dis = "0"

                col = self.db['jwalk_boundary']
                
                col.update_many({}, {"$set": {"dis_polygon": dis}}) 
                

            else:
                
                
                
                details = request.form
                
                try:
                    dis = details['dis_polygon'] 
                    
                    self.dis_polygon = True
                except:
                    self.dis_polygon = False
                
                
                document = {
                    'camera_id': id,
                    'polygon_id': self.polygon_id,
                    'x_position': details['x'],
                    'y_position': details['y'],
                    'timestamp': datetime.now(),
                    'dis_polygon': self.dis_polygon
                
                }

  

                documents = self.db['jwalk_boundary']
                document_inserted_id = documents.insert_one(document).inserted_id

        else:
            self.get_new_id()


        
        
       
        vidcap = cv2.VideoCapture(video_ip)
        success,frame = vidcap.read()
        

        col = self.db['jwalk_boundary']
        docs = col.find({'camera_id': id}).sort("timestamp")

        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)

        print("========="+id+"==========>"+str((video_ip)))
        try:
            if(len(j_data) > 2 ):
                xy_polygon = []
                polygon_id = int(j_data[0]["polygon_id"])
                self.dis_polygon = int(j_data[0]["dis_polygon"])

                for i in range(len(j_data)):
                    
                    if(polygon_id != int(j_data[i]["polygon_id"]) and i>0):

                        if(len(xy_polygon)>2):
                            polygon = Polygon(xy_polygon)
                            frame = Set_boundary.drawPolygon(frame,polygon)
                            xy_polygon = []

                    x = int(j_data[i]["x_position"])
                    y = int(j_data[i]["y_position"])
                    xy_polygon.append([x,y])

                    polygon_id = int(j_data[i]["polygon_id"])

                try:
                    polygon = Polygon(xy_polygon)
                    frame = Set_boundary.drawPolygon(frame,polygon)
                except:
                    pass
        except:
            pass
        

            
        
            
      
        global base64_img
        try:
            
            _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
            base64_img = base64.b64encode(encoded_img).decode("utf-8")
        except:
            base64_img = None
            pass
        
        return base64_img
        

    def getcameraURL(self,id):
        col = self.db['camera']
        docs = col.find({'_id': ObjectId(id)}).sort("timestamp")

        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)

       
        video_ip = ""
        server = ""
        
        if(len(j_data)>0):
            video_ip = j_data[0]["url"]
            server = j_data[0]["server"]

        return video_ip,server

    def getVideoURL(self,id):
        col = self.db['demo']
        docs = col.find({'_id': ObjectId(id)}).sort("timestamp")

        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)

       
        video_ip = ""
        
        
        if(len(j_data)>0):
            video_ip = j_data[0]["url"]

        return video_ip


    def set_counting_boundary(self,id):
        gl = General()

        #url = self.getVideoURL(id)
        id = "6157cd98451534325b4fdcaa"
        video_ip,server = self.getcameraURL(id)
        print("====id="+id+"========video_ip==>"+video_ip)
        vidcap = cv2.VideoCapture(video_ip)
        success,frame = vidcap.read()
        
        # if request.method == "POST":
            
            

        #     if  'clear_button' in request.form: 
                
        #         self.xy_polygon_counting = []
        #         self.polygon_points = ""
                

        #     elif 'add_button' in request.form: 
               
        #         details = request.form  

        #         print(details)
        #         if(details['landName'] != "" and details['polygon']!= ""):
                    
                    
        #             str_polygon = details['polygon'].split(")(")
        #             polygon_data = []
        #             for i in range(len(str_polygon)):
        #                 data = str_polygon[i].replace("(","").replace(")","")
        #                 data =data.split(",")
        #                 X = int(data[0])
        #                 Y = int(data[1])

        #                 polygon_data.append([X,Y])

                    

                    
        #             document = {
        #                 'camera_id': id,
        #                 'lane_name': details['landName'],
        #                 'lane_type': details['flexType'],
        #                 'polygon': polygon_data,
        #                 'timestamp': datetime.now()
                    
        #             }

    

        #             documents = self.db['counting_boundary']
        #             document_inserted_id = documents.insert_one(document)
        #             # request.form = None


                    
        #             self.xy_polygon_counting = []
        #             self.polygon_points = ""
        #             print("====================+> Clear")
            
            

        # col = self.db['counting_boundary']
        # docs = col.find({'camera_id': id}).sort("timestamp")

        # json_data = json_util.dumps(docs)
        # j_data = json.loads(json_data)

        # int_row =0
        # int_row = len(j_data)
        # # for i in range(len(j_data)):
            
        # #     polygon = Polygon(j_data[i]["polygon"])
        # #     frame = Set_boundary.drawPolygon(frame,polygon,gl.getColor(i))


        # land_name = ""
        # start_point = ""
        # end_point = ""
        # lane_type = ""
        # try:
        #     land_name = request.form["landName"]
        #     x = int(request.form["x"])
        #     y = int(request.form["y"])
        #     lane_type = request.form["flexType"]
        #     self.xy_polygon_counting.append([x,y])
            
            

        #     if(len(self.xy_polygon_counting) >2 ):
        #         polygon = Polygon(self.xy_polygon_counting)
        #         frame = Set_boundary.drawPolygon(frame,polygon, gl.getColor(int_row))

                
            
            
       
                   
        #     self.polygon_points += "("+str(x)+","+str(y)+")"

        # except:
        #     pass
    
        global base64_img
        try:

            
            _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
            base64_img = base64.b64encode(encoded_img).decode("utf-8")
        except:
            base64_img = None
            pass
        print("=====img = "+str(base64_img))
        return base64_img


    def set_counting_video_boundary(self,id):

        print("================> data = "+str(request.form) )
       
        frame  = requests.post('http://127.0.0.1:6001/get_image_byID/'+id)


        if request.method == "POST":
            details = request.form 

            if  'add_button' in request.form: 
                if(details['lane_name'] != "" and details['polygon']!= ""):
                                
                    document = {
                        'camera_id': id,
                        'lane_name': details['lane_name'],
                        'lane_type': details['lane_type'],
                        'start_point':self.xy_polygon_counting,
                        'timestamp': datetime.now()
                    
                    }



                    documents = self.db['counting_video_boundary']
                    document_inserted_id = documents.insert_one(document).inserted_id
                    
                    self.xy_polygon_counting = []
                    self.polygon_points = ""

            elif  'clear_button' in request.form: 
                self.xy_polygon_counting = []
                self.polygon_points = ""
               
            else:

                x = int(request.form["x"])
                y = int(request.form["y"])
                self.xy_polygon_counting.append([x,y])
               

        global base64_img
        try:
            print(len(frame))
            _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
            base64_img = base64.b64encode(encoded_img).decode("utf-8")
        except:
            base64_img = None
            pass

        return base64_img,"","",self.polygon_points
    
    
    def getVideoFrame(self,url):
        # cap = cv2.VideoCapture(url)
        # frame = None
        # if (cap.isOpened()== False): 
        #     print("Error opening video  file")
    
        # int_frame = 0
        # while(cap.isOpened()):
        
        #     # Capture frame-by-frame
        #     ret, frame = cap.read()    
        #     break
        
        
        # cap.release()
        # print("==============my frame==="+url+"===="+str(cap.isOpened()))
        # return frame

        cap = cv2.VideoCapture('./data/video/apple.mp4')
        result = None
        while(cap.isOpened()):

            ret, frame = cap.read()

            if ret==True:
                result = frame
            
                if cv2.waitKey(1) == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        print("==============my frame======="+str(cap.isOpened()))
        return result
