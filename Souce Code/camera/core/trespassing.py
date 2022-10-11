
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
import requests
import math
import time 
from datetime import datetime
import subprocess
from core.notification import Notification as notification


class Trespassing:
    
    

    def drawPolygon(frame,polygon,color):
        alpha = 0.15 # that's your transparency factor
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

    def exportVideo_Jaywalking(frame,database,out,status,event_type,bounday_id,camera_id,temp_record,file_name):

        # path = "//media/iotlab/Work/master_vision/app/web/assets/event/"+event_type
        path = "/media/iotlab/deploy/oshawa/app/web/assets/event/"+event_type

        if(out != None):
            print("out.isOpened(): "+str(out.isOpened())+", status= "+status)
            if(out.isOpened() and status == "create"):
                status = "write"

            if(out.isOpened() == False and status == "close"):
                return out
        else:
             status == "create"

        if status == "create":

            # timestamp = datetime.now()
            # file_name = timestamp.strftime("%Y%m%d-%H%M%S")+".avi"
            # 
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            h, w, c = frame.shape
            
            video_name = path+"/"+camera_id+".mp4"
            out = cv2.VideoWriter(video_name,fourcc, 8, (w, h))
            

            
            #### Save Event
            

            #### write temp

            for tmp in temp_record:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(tmp)

        elif status == "close":
            

            new_file =  path+"/"+file_name 
            old_file =  path+"/"+camera_id+".mp4" 
            print("new = "+ new_file +"  , old = "+old_file)
            out.release()
            str_exe = "ffmpeg -i "+old_file+" -vcodec h264 -acodec mp2 "+new_file
            # subprocess.Popen( ["lxterminal", "-e", str_exe])


            os.popen(str_exe)
            saveEvent(database,bounday_id,file_name)
            # subprocess.Popen( ['lxterminal', '-e', 'ffmpeg -i '+path+'/'+bounday_id+".mp4"+' -vcodec h264 -acodec mp2 '+path+'/'+file_name ])
            # try:
            #     noti = notification()
            #     noti.send_notification_email(file_name,temp_record[0],"Jaywalking")
            # except:
            #     pass


            # frame_convert = cv2.cvtColor(temp_record[0], cv2.COLOR_RGB2BGR)
            

        elif status == "write":
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            try:
                out.write(frame)
            except:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                timestamp = datetime.now()
                h, w, c = frame.shape
                
                video_name = file_name
                
                out = cv2.VideoWriter(path+"/"+camera_id+".mp4",fourcc,8, (w, h))
                out.write(frame)
            
        return out
#########################  Jaywalking ################

    def  Jaywalking_couting_detection(frame,database,lanes,boxes,classes,confidences,previous_frame,start_time,count_jaywalking,out,temp_record,file_name,status):

        raw_frame = None
        #current_images = []    
        str_text = ""
        gl = General()
        font = cv2.FONT_HERSHEY_SIMPLEX
        all_person = previous_frame
      

        int_row = 0

        int_person = 0
        
        # for cls in classes:
        #     if(cls== "person"):
        #         int_person+=1
        
        
        
        
        for lane in lanes:
            
            if(lane.lane_type != "jaywalking"):
                continue
            
            all_images = []

            person_point = []
            polygon = Polygon(lane.polygon)
            frame = Trespassing.drawPolygon(frame,polygon,(255, 234, 0))
            center = polygon.centroid.coords
            X_text = int(center[0][0])
            Y_text = int(center[0][1])

            int_person=0
            
           
            

                    
            int_row+=1
            int_bb = 0

            int_vehicle_inside = 0
            int_index = 0
            old_time = time.time()

            ind_person = 0

            int_check = 0
            for pre in previous_frame:
                
                if(pre[1] < -10):
                    previous_frame.pop(int_check)
                    print("============================++> Done")
                    if(status == "write"):
                        status = "close"
                    break
                else:
                    pre[1]-=1
                int_check+=1


            for bbox in boxes:
               
                W = int(bbox[2])
                H = int(bbox[3])
                X = int(bbox[0])
                Y = int(bbox[1])
          

               

                if(classes[int_index] != "person"):
                    cv2.rectangle(frame, (X, Y), (X+W,Y+H), (0,0,255), 1)
                    cv2.rectangle(frame, (X, Y-10), (X+W, Y),  (0,0,255), -1)

                    cv2.putText(frame, classes[int_index]+"-"+str(round(confidences[int_index]*100,2))+"%", (X,Y),  cv2.FONT_HERSHEY_PLAIN, 
                            0.8,(255,255,255), 1)

                if(classes[int_index] == "person"):

                    
                    

                    point = point_shape(X+int(W/2), Y+int(H/2))

                    result = polygon.contains(point)

                    
                    
                    


                    
                    
                    if result:
                        
                        
                        color = gl.getColorDetect(2)


                        cv2.rectangle(frame, (X, Y), (X+W,Y+H), color, 1)
                        cv2.rectangle(frame, (X, Y-10), (X+W, Y),  color, -1)

                        cv2.putText(frame, classes[int_index]+"-"+str(round(confidences[int_index]*100,2))+"%", (X,Y),  cv2.FONT_HERSHEY_PLAIN, 
                                0.8,(255,255,255), 1)

                        
                        int_person+=1
                        
                        person_point.append([X,Y+H])
                        max_score = 0
                    
                        
                        
                        


                        previous_lane = [] 
                        bool_old = False
                        for pre in previous_frame:
                            if(lane.lane_name == pre[0]):
                                if(pre[1] < 50):
                                    pre[1] += 10
                                bool_old = True

                        if(not bool_old):
                            all_person.append([lane.lane_name,5])
                                
                        previous_frame[0][1]
                int_index+=1
                    
            if(int_person == 0):
                lane.check_no_vehicle +=1
            
            

            diff_time = time.time() - start_time
            if diff_time >5  and int_person == 0:
                count_jaywalking = 0
                
            

            if( int(diff_time) >=0 and int(diff_time) <=20):

                if(len(previous_frame) > 0):

                    if int(previous_frame[0][1]) > 30:
                        if(count_jaywalking > 0):
                            if(status == ""):
                                status = "create"
                                lane.totalCount  = lane.totalCount + 1
                                
                       
                            else:
                                status = "write"

                    elif (count_jaywalking == 0 and previous_frame[0][1] < -10 and status!= ""):
                        status = "close"
                        timestamp = datetime.now()
                        file_name = timestamp.strftime("%Y%m%d-%H%M%S")+".mp4"
                        Trespassing.saveJaywalking(database,lane.boundary_id,file_name)


                    print("count_jaywalking= "+str(count_jaywalking)+ ", previous_frame = "+str(len(previous_frame))+ 
                            " , previous_frame[0][1]: "+str(int(previous_frame[0][1])) + " , status= "+status)


            if  int_person > count_jaywalking and diff_time > 10 :
                
                start_time = time.time()
            
                
                # print("=====lane= "+lane.lane_name+"===>inside: "+str(int_person) + "   max= "+str(count_jaywalking) + " diff_time="+str(diff_time))

                # if (int_person-count_jaywalking > 0 and status != ""):
                    
                    # lane.totalCount  = lane.totalCount + 1
                    
                # print("===previous="+str(len(previous_lane)) + " person:"+str(int_person))
                
            if(int_person > 0):
                start_time = time.time()
                
                

            if(int_person > 0):
                count_jaywalking = int_person
                # lane.totalCount = int_person

            # print("====="+lane.lane_name+"===inside= "+str(int_person)+"===count_jaywalking="+str(count_jaywalking) + "  diff"+str(diff_time))


            

            
                    

                    
                        
        
            
            raw_frame = frame.copy()

            cv2.putText(frame,str(lane.lane_name), (X_text,Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5,(255,255,255), 1)
            cv2.putText(frame,str(lane.totalCount), (X_text,Y_text-5),  cv2.FONT_HERSHEY_SIMPLEX, 
                    1,(255,255,255), 3)
        # frame = Trespassing.countJaywalking(areas,frame,camera_id)
        
       
        
        # 
        if(status != ""):
            # raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR)
            out = Trespassing.exportVideo_Jaywalking(raw_frame,database,out,status,"jaywalking",lane.boundary_id,lane.camera_id,temp_record,file_name)
        
            if status== "close":
                file_name= ""
                status = ""

        if(len(temp_record) >30):
            
            temp_record.pop(0)
        raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR)
        temp_record.append(raw_frame)

        return frame,all_person,start_time,count_jaywalking,out,temp_record,lanes,file_name,status

    

    def saveJaywalking(database,boundary_id,file_name):
        object_ = {
            'boundary_id': boundary_id,
            'class_name': "jaywalker",
            'file_name':file_name
        }
        requests.post(database+"/vehicle_counting/store", data = object_)


######################### ENd  Jaywalking ################


def saveEvent(database,boundary_id,file_name):

    object_ = {
            'boundary_id': boundary_id,
            'file_name': file_name
        }
    print("Save Jaywalking")
    requests.post(database+"/save_event/store", data = object_)






