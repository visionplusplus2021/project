
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
class Trespassing:
    
    

    def drawPolygon(frame,polygon,color):
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

    def exportVideo_Jaywalking(frame,database,out,status,event_type,bounday_id,temp_record):

        if(out != None):
            if(out.isOpened() and status == "create"):
                status = "write"

            if(out.isOpened() == False and status == "close"):
                return out
        else:
             status == "create"
        
        if status == "create":
            print("Create file")
            timestamp = datetime.now()
            file_name = timestamp.strftime("%Y%m%d-%H%M%S")+".mp4"
            saveEvent(database,bounday_id,file_name)
            print("Save jaywalking event")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            h, w, c = frame.shape
            
            path = "/media/iotlab/Work/master_vision/app/web/assets/event/"+event_type
            video_name = file_name
            out = cv2.VideoWriter(path+"/"+video_name,fourcc, 10, (w, h))
            

            
            #### Save Event
            

            #### write temp

            for tmp in temp_record:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(tmp)

        elif status == "close":
            try:
                out.release()
            except:
                pass

        elif status == "write":
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            try:
                out.write(frame)
            except:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                timestamp = datetime.now()
                h, w, c = frame.shape
                file_name = timestamp.strftime("%Y%m%d-%H%M%S")+".avi"
                video_name = file_name
                out = cv2.VideoWriter("events/"+event_type+"/"+video_name,fourcc, 3.0, (w, h))
                out.write(frame)
            
        return out
#########################  Jaywalking ################
    def countJaywalking(areas,frame,camera_id):
        gl = General()
        dbMain = 'mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
    
        col = db['jaywalking_count']
        docs = col.aggregate([ { "$match" : { "camera_id" : camera_id } },
                                {
                            "$group" : 
                                {"_id" : {"camera_name":"$camera_name","area_name":"$area_name"}, 
                                "area_name" : {"$first":"$area_name"}, 
                                "total" : {"$sum" : 1}
                                }}
                            ])

                            
        
        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)

        

        int_row = 0


        int_lane = 0
        for area in areas:

            
            
            int_count = 0
           
            for i in range(len(j_data)):
                
                if(area.area_name == j_data[i]["area_name"]):

                    int_count = j_data[i]["total"]

                    
                    break
            
            
            polygon = Polygon(area.polygon)
            center = polygon.centroid.coords
            X_text = int(center[0][0])
            Y_text = int(center[0][1])

            cv2.putText(frame,str(area.area_name), (X_text+ (len(str(int_count))*5),Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                   0.3,(225,225,225), 1)
            cv2.putText(frame,str(int_count), (X_text-20,Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6,(255,255,255), 2)


            int_row+=1
            int_lane+=1
           
         
        return frame
    
    
    def  Jaywalking_couting_detection(frame,database,lanes,boxes,classes,confidences,previous_frame,start_time,count_jaywalking,out,temp_record):

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
            
           
            cv2.putText(frame,str(lane.lane_name), (X_text,Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5,(225,225,225), 1)
            cv2.putText(frame,str(lane.totalCount), (X_text,Y_text-5),  cv2.FONT_HERSHEY_SIMPLEX, 
                    1,(255,255,255), 2)

                    
            int_row+=1
            int_bb = 0

            int_vehicle_inside = 0
            int_index = 0
            old_time = time.time()

            ind_person = 0

            int_check = 0
            for pre in previous_frame:
                
                if(pre[1] < -100):
                    previous_frame.pop(int_check)
                    break
                else:
                    pre[1]-=1
                int_check+=1


            for bbox in boxes:
               
                if(classes[int_index] == "person"):

               
                    W = int(bbox[2])
                    H = int(bbox[3])
                    X = int(bbox[0]) +int(W/4)
                    Y = int(bbox[1])+int(H/4)
               
                    point = point_shape(X+10, Y+int(H/2)-10)

                    result = polygon.contains(point)

                    


                    
                    
                    if result:
                        color = gl.getColorDetect(0)
                        cv2.rectangle(frame, (X, Y), (X+int(W/2),Y+int(H/2)), color, 1)
                        cv2.rectangle(frame, (X, Y-10), (X+int(W/2), Y),  color, -1)
                        
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

            if  int_person > count_jaywalking and diff_time > 10 :
                
                start_time = time.time()
            

                # print("=====lane= "+lane.lane_name+"===>inside: "+str(int_person) + "   max= "+str(count_jaywalking) + " diff_time="+str(diff_time))

                for i in range(int_person-count_jaywalking):
                    Trespassing.saveJaywalking(database,lane.boundary_id)
                    lane.totalCount  = lane.totalCount + 1
                # print("===previous="+str(len(previous_lane)) + " person:"+str(int_person))
                
            if(int_person > 0):
                start_time = time.time()
                

            if(int_person > 0):
                count_jaywalking = int_person
                lane.totalCount = int_person

            # print("====="+lane.lane_name+"===inside= "+str(int_person)+"===count_jaywalking="+str(count_jaywalking) + "  diff"+str(diff_time))


            status = ""
            
            if( int(diff_time) >=0 and int(diff_time) <=20):

                if(len(previous_frame) > 0):
                    print("previous_frame[0][1] "+ str(previous_frame[0][1]))

                    if(int(previous_frame[0][1]) > 5  and status == ""):
                        status = "create"
                    elif (previous_frame[0][1] < 0):
                        status = "close"
                    else:
                        status = "write"
        
        
            if(status != ""):
                
                out = Trespassing.exportVideo_Jaywalking(frame,database,out,status,"jaywalking",lane.boundary_id,temp_record)
            
        
        # frame = Trespassing.countJaywalking(areas,frame,camera_id)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if(len(temp_record) >50):
            
            temp_record.pop(0)
        temp_record.append(frame)

        #print("==++>"+str(len(temp_record)))
        return frame,all_person,start_time,count_jaywalking,out,temp_record,lanes


    # def Jaywalking_couting_detection(frame,areas,boxes,classes,camera_id,camera_name,self,confidence,ids,previous_frame,count_jaywalking,start_time,out):

    #     #current_images = []
    #     str_text = ""
    #     gl = General()
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     all_vehicle = []
      

    #     int_row = 0

    #     int_person = 0
        
    #     # for cls in classes:
    #     #     if(cls== "person"):
    #     #         int_person+=1
            
        
    #     for area in areas:
            
            
    #         all_images = []

    #         vehicle_point = []
    #         polygon = Polygon(area.polygon)
    #         frame = Trespassing.drawPolygon(frame,polygon,(255, 234, 0))
    #         center = polygon.centroid.coords
    #         X_text = int(center[0][0])
    #         Y_text = int(center[0][1])

    #         int_person=0
            
    #         x = area.polygon[0][0]
    #         y = area.polygon[0][1]
            
    #         int_row+=1
    #         int_bb = 0

    #         int_vehicle_inside = 0
    #         int_index = 0
    #         old_time = time.time()

    #         ind_person = 0
    #         for bbox in boxes:
               
    #             if(classes[int_index] == "person"):

               
    #                 X = int(bbox[0]) 
    #                 Y = int(bbox[1])
    #                 W = int(bbox[2])
    #                 H = int(bbox[3])
    #                 point = point_shape(X+10, Y+H-10)

    #                 result = polygon.contains(point)

                    


                    
                    
    #                 if result:
    #                     color = gl.getColorDetect(0)
                

    #         #     #     color = [i * 255 for i in color]
    #                     cv2.rectangle(frame, (X, Y), (X+W,Y+H), color, 1)
    #                     cv2.rectangle(frame, (X, Y-10), (X+W,Y+5 ),  color, -1)
                        
    #                     cv2.putText(frame, classes[int_index]+"-"+str(round(confidence[int_index]*100,2))+"%", (X,Y),  cv2.FONT_HERSHEY_PLAIN, 
    #                     0.8,(255,255,255), 1)

                        
    #                     int_person+=1
                        
    #                     vehicle_point.append([X,Y+H])
    #                     max_score = 0
                    
    #                     all_vehicle.append([None,area.area_name,""])
                        
                        


                    
    #                     previous_lane = [] 
    #                     for pre in previous_frame:
    #                         if(area.area_name == pre[1]):
    #                             previous_lane.append(pre)
                                
                    

    #                     if(len(previous_lane) > 0 ):
    #                         dist = 0
    #                         area.check_no_vehicle = 0
    #                         if(len(vehicle_point) > 1 ):
    #                             x1 = vehicle_point[0][0]
    #                             y1 = vehicle_point[0][1]
    #                             x2 = vehicle_point[1][0]
    #                             y2 = vehicle_point[1][1]


    #                             dist = math.hypot(x2 - x1, y2 - y1)

    #                         max_score = 1
                        

                    
    #                             #break
                    
                    


    #                 else:
    #                     area.check_no_vehicle += 1

    #                     #print("lane:"+area.area_name+ " ==> empty:"+str(lane.check_no_vehicle))

    #             int_index+=1
                    
    #         if(int_person == 0):
    #             area.check_no_vehicle +=1
            
            

    #         diff_time = time.time() - start_time
    #         if diff_time >5  and int_person == 0:
    #             count_jaywalking = 0

    #         if  int_person > count_jaywalking and diff_time > 10 :
                
    #             start_time = time.time()
            

    #             print("=====lane= "+area.area_name+"===>inside: "+str(int_person) + "   max= "+str(count_jaywalking) + " diff_time="+str(diff_time))

    #             for i in range(int_person-count_jaywalking):
    #                 Trespassing.saveJaywalking(area.area_name,self._id,self.camera_name)
    #             print("===previous="+str(len(previous_lane)) + " person:"+str(int_person))
                
    #         if(int_person > 0):
    #             start_time = time.time()
                

    #         if(int_person > 0):
    #             count_jaywalking = int_person
    #             area.totalCount = int_person

    #     print("====="+area.area_name+"===inside= "+str(int_person)+"===count_jaywalking="+str(count_jaywalking) + "  diff"+str(diff_time))
    #     status = ""

    #     if( int(diff_time) >=0 and int(diff_time) <=20):
    #         if(int(diff_time) == 0):
    #             status = "create"
    #         elif (count_jaywalking == 0 and  diff_time > 10 ):
    #             status = "close"
    #         else:
    #             status = "write"
        
        
    #     if(status != ""):
            
    #         out = Trespassing.exportVideo_Jaywalking(frame,out,status,"jaywalking",self.server,camera_id,camera_name)
    #     frame = Trespassing.countJaywalking(areas,frame,camera_id)
    #     return frame,all_vehicle,count_jaywalking,start_time,out

    def saveJaywalking(database,boundary_id):
        object_ = {
            'boundary_id': boundary_id,
            'class_name': "person"
        }
        requests.post(database+"/vehicle_counting/store", data = object_)


######################### ENd  Jaywalking ################


#########################  Trespassing ################

    def countTrespassing(areas,frame,camera_id):
        gl = General()
        dbMain = 'mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
    
        col = db['trespassing_count']
        docs = col.aggregate([ { "$match" : { "camera_id" : camera_id } },
                                {
                            "$group" : 
                                {"_id" : {"camera_name":"$camera_name","area_name":"$area_name"}, 
                                "area_name" : {"$first":"$area_name"}, 
                                "total" : {"$sum" : 1}
                                }}
                            ])

                            
        
        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)

        

        int_row = 0


        int_lane = 0
        for area in areas:

            
            
            int_count = 0
           
            for i in range(len(j_data)):
                
                if(area.area_name == j_data[i]["area_name"]):

                    int_count = j_data[i]["total"]

                    
                    break
            
            
            polygon = Polygon(area.polygon)
            center = polygon.centroid.coords
            X_text = int(center[0][0])
            Y_text = int(center[0][1])

            cv2.putText(frame,str(area.area_name), (X_text+ (len(str(int_count))*5),Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                   0.3,(225,225,225), 1)
            cv2.putText(frame,str(int_count), (X_text-20,Y_text+10),  cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6,(255,255,255), 2)


            int_row+=1
            int_lane+=1
           
         
        return frame

    def Trespassing_couting_detection(frame,areas,boxes,classes,camera_id,camera_name,self,confidence,ids,previous_frame,count_jaywalking,start_time,out):

        #current_images = []
        str_text = ""
        gl = General()
        font = cv2.FONT_HERSHEY_SIMPLEX
        all_vehicle = []
      

        int_row = 0

        int_person = 0
        
        # for cls in classes:
        #     if(cls== "person"):
        #         int_person+=1
            
        
        for area in areas:
            
           
            all_images = []

            vehicle_point = []
            polygon = Polygon(area.polygon)
            frame = Trespassing.drawPolygon(frame,polygon,gl.getColorLabel(int_row))



            center = polygon.centroid.coords
            X_text = int(center[0][0])
            Y_text = int(center[0][1])

            int_person=0
            
            x = area.polygon[0][0]
            y = area.polygon[0][1]
            
            int_row+=1
            int_bb = 0

            int_vehicle_inside = 0
            int_index = 0
            old_time = time.time()

            ind_person = 0
            for bbox in boxes:
               
                if(classes[int_index] == "person"):

                    
                    X = int(bbox[0]) 
                    Y = int(bbox[1])
                    W = int(bbox[2])
                    H = int(bbox[3])
                    point = point_shape(X+10, Y+H-10)

                    result = polygon.contains(point)

                    color = gl.getColorDetect(0)
        #     #     color = [i * 255 for i in color]
                    cv2.rectangle(frame, (X, Y), (X+W,Y+H), color, 1)
                    cv2.rectangle(frame, (X, Y-10), (X+W,Y+5 ),  color, -1)
                    
                    cv2.putText(frame, classes[int_index]+"-"+str(round(confidence[int_index]*100,2))+"%", (X,Y),  cv2.FONT_HERSHEY_PLAIN, 
                    0.8,(255,255,255), 1)

                    
                    
                    if result:
                        

                        
                        int_person+=1
                        
                        vehicle_point.append([X,Y+H])
                        max_score = 0
                    
                        all_vehicle.append([None,area.area_name,""])
                        
                        


                    
                        previous_lane = [] 
                        for pre in previous_frame:
                            if(area.area_name == pre[1]):
                                previous_lane.append(pre)
                                
                    

                        if(len(previous_lane) > 0 ):
                            dist = 0
                            area.check_no_vehicle = 0
                            if(len(vehicle_point) > 1 ):
                                x1 = vehicle_point[0][0]
                                y1 = vehicle_point[0][1]
                                x2 = vehicle_point[1][0]
                                y2 = vehicle_point[1][1]


                                dist = math.hypot(x2 - x1, y2 - y1)

                            max_score = 1
                        

                    
                                #break
                    
                    


                    else:
                        area.check_no_vehicle += 1

                        #print("lane:"+area.area_name+ " ==> empty:"+str(lane.check_no_vehicle))

                int_index+=1
                    
            if(int_person == 0):
                area.check_no_vehicle +=1
            
            

            

            
            diff_time = time.time() - start_time
            if diff_time >5  and int_person == 0:
                count_jaywalking = 0

            if  int_person > count_jaywalking and diff_time > 10 :
                
                start_time = time.time()
            

                # print("=====lane= "+area.area_name+"===>inside: "+str(int_person) + "   max= "+str(count_jaywalking) + " diff_time="+str(diff_time))

                for i in range(int_person-count_jaywalking):
                    Trespassing.saveTrespassing(area.area_name,self._id,self.camera_name)
                # print("===previous="+str(len(previous_lane)) + " person:"+str(int_person))
                
            if(int_person > 0):
                start_time = time.time()
                

            if(int_person > 0):
                count_jaywalking = int_person
                area.totalCount = int_person

        # print("====="+area.area_name+"===inside= "+str(int_person)+"===count_jaywalking="+str(count_jaywalking) + "  diff"+str(diff_time))
        status = ""

        if( int(diff_time) >=0 and int(diff_time) <=20):
            if(int(diff_time) == 0):
                status = "create"
            elif (count_jaywalking == 0 and  diff_time > 10 ):
                status = "close"
            else:
                status = "write"
        
        
        if(status != ""):
            
            out = Trespassing.exportVideo_Jaywalking(frame,out,status,"trespassing",self.server,camera_id,camera_name)


        frame = Trespassing.countTrespassing(areas,frame,camera_id)
        return frame,all_vehicle,count_jaywalking,start_time,out

    def saveTrespassing(area_name,camera_id,camera_name):
        object_ = {
            
            'area_name': area_name,
            'camera_id': camera_id,
            'camera_name': camera_name
        }
        requests.post('http://172.21.12.132:9001/trespassing_count/store', data = object_)

######################### End Trespassing ################

def saveEvent(database,boundary_id,file_name):

    object_ = {
            'boundary_id': boundary_id,
            'file_name': file_name
        }
    print("Save Jaywalking")
    requests.post(database+"/save_event/store", data = object_)

    # object_ = {
        
    #     'event_type': event_type,
    #     'file_name': file_name,
    #     'server': server,
    #     'camera_id': camera_id,
    #     'camera_name': camera_name,
    # }
    # requests.post('http://172.21.12.132:9001/event/store', data = object_)


    
def person_detection(frame, bboxes, scores, names,camera_ip):

    bool_detected = False
    alpha = 0.5 # that's your transparency factor
    (H, W) = frame.shape[:2]

    xmin = 0
    ymin = 0 
    xmax = int(W / 2)
    ymax = int(H / 2)

    dbMain = 'mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    client = pymongo.MongoClient(dbMain)
    db = client['test']

    col = db['boundary']

    results = col.find()
    output = []

    docs = col.find({"camera_id":camera_ip}).sort("timestamp")

    json_data = json_util.dumps(docs)
    j_data = json.loads(json_data)

    
    if(len(j_data) > 2 ):
        xy_polygon = []
        polygon_id = int(j_data[0]["polygon_id"])
        dis_polygon = int(j_data[0]["dis_polygon"])

        for i in range(len(j_data)):
            
            if(polygon_id != int(j_data[i]["polygon_id"]) and i>0):

                if(len(xy_polygon)>2):
                    polygon = Polygon(xy_polygon)
                    frame = Trespassing.drawPolygon(frame,polygon,(0, 0, 255))
                    xy_polygon = []

            x = int(j_data[i]["x_position"])
            y = int(j_data[i]["y_position"])
            xy_polygon.append([x,y])

            polygon_id = int(j_data[i]["polygon_id"])

        try:
            polygon = Polygon(xy_polygon)
            frame = Trespassing.drawPolygon(frame,polygon,(0, 0, 255))
        except:
            pass
    else:
        
        return frame,bool_detected

    
    for i in range(len(names)):
        if(names[i] == "person"):
        
            x_point = int(bboxes[i][0] + (bboxes[i][2]/2))
            y_point = int(bboxes[i][1] + bboxes[i][3])
            center_coordinates = (x_point,y_point-10)
            
            

        #point = point_shape(lat, lon)
            
            point = point_shape(x_point, y_point-10)
            bool_inside = polygon.contains(point)
            if(bool_inside): 
                frame = cv2.circle(frame, center_coordinates, 2, (255, 0, 0), 5)
                x_text = int(bboxes[i][0])
                y_text = int(bboxes[i][1])-10
                if(y_text < 10):
                    y_text = 10
                cv2.putText(frame,"Intruder",(x_text,y_text ),0, 0.8, (255,255,255),1)
                
                x =  int(bboxes[i][0])
                y = int(bboxes[i][1])
                x2 = int(bboxes[i][0])+int(bboxes[i][2])
                y2 = int(bboxes[i][1])+int(bboxes[i][3])

                cv2.rectangle(frame,(x,y) ,(x2 , y2), (255,0,0), 2)



            else:
                frame = cv2.circle(frame, center_coordinates, 2, (0, 255, 0), 5)

    
    return frame,bool_detected

    


