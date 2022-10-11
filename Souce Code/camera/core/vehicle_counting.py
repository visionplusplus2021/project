import time 
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
import matplotlib.pyplot as plt
import requests
import math 
import pprint

from skimage.metrics import structural_similarity as compare_ssim


class VehicleCounting:

    def drawPolygon(self,frame,polygon,color):
        alpha = 0.25 # that's your transparency factor
        (H, W) = frame.shape[:2]

        xmin = 0
        ymin = 0 
        xmax = int(W / 2)
        ymax = int(H / 2)

        
        int_coords = lambda x: np.array(x).round().astype(np.int32)
        exterior = [int_coords(polygon.exterior.coords)]

        overlay = frame.copy()
        cv2.fillPoly(overlay, exterior, color=color)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        return frame
    
    def saveVehicle(self,database,boundary_id,class_name):
        object_ = {
            'boundary_id': boundary_id,
            'class_name': class_name,
            'file_name':""
        }
        requests.post(database+"/vehicle_counting/store", data = object_)


    def selectLane(self,database,camera_feature_id):
        docs = requests.get(database+'/camera/getBoundaryByCameraID/'+camera_feature_id)
        j_data = json.loads(docs.content) 
        return j_data

    def selectVehicleCounting(self,database,camera_feature_id):
        docs = requests.get(database+'/camera/getVehicleCountingByCameraID/'+camera_feature_id)
        j_data = json.loads(docs.content) 
        return j_data

    def selectCamerabyStreamID(self,database,streamID):
        docs = requests.get(database+'/camera/getCamerabyStreamID/'+streamID)
        j_data = json.loads(docs.content) 
        return j_data

    def selectVideoDemoFileID(self,database,fileID):
        docs = requests.get(database+'/video_demo/getFileID/'+fileID)
        j_data = json.loads(docs.content) 
        return j_data


    def countVehicle(self,database,frame,lanes):
        gl = General()
        
        print(str(lanes[0]))
        docs = requests.get(database+'/counting_vehicle/getbyCameraID/'+lanes[0].camera_id)
        j_data = json.loads(docs.content) 
        

        

        
        int_lane_count =[0,0,0,0,0]

        int_row = 0

        

        
        max_name = 0
        

        int_lane = 0
        for lane in lanes:

            

            int_count = 0

            for data in j_data:
                print("lane.lane_name="+lane.lane_name+" , "+ data[1])
                if(lane.lane_name == data[1]):
                    int_count = data[2]
                    break


                
            # for i in range(len(j_data)):
                
            #     if(lane.lane_name == j_data[0][i][1]):

            #         int_count = j_data[0][i][2]

                    
            #         break
            
            
            polygon = Polygon(lane.polygon)
            center = polygon.centroid.coords
            X_text = int(center[0][0])
            Y_text = int(center[0][1])

            cv2.putText(frame,str(lane.lane_name), (X_text,Y_text+5),  cv2.FONT_HERSHEY_SIMPLEX, 
                   0.3,(225,225,225), 1)
            cv2.putText(frame,str(int_count), (X_text,Y_text-5),  cv2.FONT_HERSHEY_SIMPLEX, 
                   0.4,(255,255,255), 1)

            int_row+=1
            int_lane+=1
           
         
        return frame


    def vehicle_couting_detection(self,frame,database,lanes,boxes,classes,class_indexs,confidences,previous_frame,deeps):

        #current_images = []
        str_text = ""
        gl = General()
        font = cv2.FONT_HERSHEY_SIMPLEX
        all_vehicle = previous_frame
      
        
        int_row = 0
        int_index = 0
        if(len(lanes)) == 0:
            for bbox in boxes:  

                W = int(bbox[2])
                H = int(bbox[3])
                X = int(bbox[0]) 
                Y = int(bbox[1])
               
                point = point_shape(X+10, Y+int(H/2))

                check_points = []

                color = gl.getColorDetect (0)
                #cv2.circle(frame,(X+10, Y+int(H/2)), 2, (0, 0, 255), 3)

                cv2.rectangle(frame, (X, Y), (X+int(W/2),Y+int(H/2)), color, 1)
                cv2.rectangle(frame, (X, Y-10), (X+int(W/2), Y),  color, -1)

                cv2.putText(frame, classes[int_index]+"-"+str(round(confidences[int_index]*100,2))+"%", (X,Y),  cv2.FONT_HERSHEY_PLAIN, 
                   0.8,(255,255,255), 1)
                
                int_index +=1
                
            return frame,all_vehicle,lanes

        #lanes_count = self.selectVehicleCounting(database,lanes[0].camera_id)
       

        tracks = deeps.tracker_tracks(frame, boxes, confidences, classes)

        

            #cv2.circle(frame,(int(track_bbox[0]), int(track_bbox[1])), 10, (255, 0, 0), 10)
            #print("====track_id ===+++> "+str(track_bbox))
        bool_vehicle = False
        bool_pedestrian = False
        
        for lane in lanes:
            if lane.lane_type == "vehicle":
                bool_vehicle = True
            elif lane.lane_type == "pedestrian":
                bool_pedestrian = True


        int_index = 0
        for bbox in boxes:  

            W = int(bbox[2])
            H = int(bbox[3])
            X = int(bbox[0])
            Y = int(bbox[1])
            
            point = point_shape(X+10, Y+int(H/2))

            check_points = []

            color = gl.getColorDetect (0)
            # cv2.circle(frame,(X, Y), 2, (255, 0, 0), 5)

            if( (classes[int_index] != "person" and bool_vehicle) or 
            (classes[int_index] == "person" and bool_pedestrian) ) :
                cv2.rectangle(frame, (X, Y), (X+W,Y+H), color, 1)
                cv2.rectangle(frame, (X, Y-10), (X+W, Y),  color, -1)

                cv2.putText(frame, classes[int_index]+"-"+str(round(confidences[int_index]*100,2))+"%", (X,Y),  cv2.FONT_HERSHEY_PLAIN, 
                    0.8,(255,255,255), 1)
            int_index+=1
            
        for lane in lanes:

            if(lane.lane_type != "vehicle" and lane.lane_type != "pedestrian"):
                continue
            
            all_images = []

            vehicle_point = []
            #polygon = Polygon(lane.polygon)
            frame = VehicleCounting.drawPolygon(self,frame,lane.polygon,lane.color)


            ### Center of Polygon
            center = lane.polygon.centroid.coords
            X_text = int(center[0][0])
            Y_text = int(center[0][1])

            
            

            

            
            # print(lane.polygon)
            
            # x = lane.polygon[0][0]
            # y = lane.polygon[0][1]
            
            int_row+=1
           
            cmap = plt.get_cmap('tab20b')
            colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]
            

            int_bb = 0

            int_vehicle_inside = 0
            int_index = 0
            old_time = time.time()
            
            int_check = 0
            for pre in previous_frame:
                if(pre[1] < -100):
                    previous_frame.pop(int_check)
                    break
                else:
                    pre[1]-=1
                int_check+=1
                

            

            old_polygon = [] 

            
            print("=======tracks "+str(len(tracks))+"====+++++++> previous_frame: "+ str(previous_frame))   
            for track in tracks:

                
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue

                track_bbox = track.to_tlbr()
                track_class = track.get_class()
                track_id = track.track_id

                
                W = int((track_bbox[2] -track_bbox[0] ) )
                H = int((track_bbox[3] -track_bbox[1]))

                X = int(track_bbox[0]) 
                Y = int(track_bbox[1]) 

                color = gl.getColorDetect (int_index)

                
                

                # cv2.putText(frame, str(track.track_id), (X+W,Y+H),  cv2.FONT_HERSHEY_PLAIN, 
                #     2,(0,0,255), 2)

                if(track_class != "person"):
                    point = point_shape(X, Y+H)
                    point2 = point_shape(X+W, Y+H-20)
                    # cv2.circle(frame,(X, Y+H), 1, (0, 150,0), 5)
                    # cv2.circle(frame,(X+W, Y+H-20), 1, (255, 0,0), 5)

                else:
                    person_x = X +int(W/2)
                    person_y = Y+H-10
                    point = point_shape(person_x, person_y)
                    point2 = point
                    # cv2.circle(frame,(person_x, person_y), 5, (0, 150,0), 5)

                # print("track_id = "+str(track_id)+ " , pre"+str(previous_frame))
                result = lane.polygon.contains(point)
                
                if(not result):
                    result = lane.polygon.contains(point2)
                

                
              

                
                
                

                if(result):

                    # cv2.circle(frame,(X+10, Y+H), 5, (150, 0,150), 5)

                    if ( (lane.lane_type == "vehicle" and track_class != "person") or 
                                 (lane.lane_type == "pedestrian" and track_class == "person")):

                        previous_lane = [] 
                        bool_old = False

                        
                        for pre in previous_frame:
                            if(track_id == pre[0]):
                                pre[1] = 10
                                #all_vehicle.append([track_id)
                                bool_old = True
                                break
                        
                        if(not bool_old):
                            all_vehicle.append([track_id,5])
                            lane.totalCount  = lane.totalCount + 1
                            self.saveVehicle(database,lane.boundary_id,track_class)

            cv2.putText(frame,str(lane.lane_name), (X_text-20,Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                0.5,(255,255,255), 1)
            cv2.putText(frame,str(lane.totalCount), (X_text-30,Y_text-5),  cv2.FONT_HERSHEY_SIMPLEX, 
                1,(255,255,255), 3)
                            
                     
        return frame,all_vehicle,lanes
        
    
        