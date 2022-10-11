import cv2
from shapely.geometry import Polygon
from shapely.geometry import Point as point_shape
import numpy as np

class FireDetection:
    

    def drawPolygon(frame,polygon,p_color):
        alpha = 0.2 # that's your transparency factor
        (H, W) = frame.shape[:2]

        xmin = 0
        ymin = 0 
        xmax = int(W / 2)
        ymax = int(H / 2)

        
        int_coords = lambda x: np.array(x).round().astype(np.int32)
        exterior = [int_coords(polygon.exterior.coords)]

        overlay = frame.copy()
        cv2.fillPoly(overlay, exterior, color=p_color)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        return frame

    def fire_detection(frame, bboxes, scores, names):

        alpha = 0.5 # that's your transparency factor
        (H, W) = frame.shape[:2]

        xmin = 0
        ymin = 0 
        xmax = int(W / 2)
        ymax = int(H / 2)

        
       
        for i in range(len(names)):
               
            x =  int(bboxes[i][0])
            y = int(bboxes[i][1])
            x2 = int(bboxes[i][0])+int(bboxes[i][2])
            y2 = int(bboxes[i][1])+int(bboxes[i][3])
            print(str(x)+","+str(y)+","+str(x2)+","+str(y2))
            
            polygon = Polygon([(x,y),(x2,y),(x2,y2),(x,y2)])
            
            
    
            
            if(names[i]== "fire"):
                cv2.rectangle(frame,(x,y) ,(x2 , y2), (255,0,0), 2)
                frame = FireDetection.drawPolygon(frame,polygon,(255,0,0))
            else:
                cv2.rectangle(frame,(x,y) ,(x2 , y2), (50,50,50), 2)
                frame = FireDetection.drawPolygon(frame,polygon,(50,50,50))
            cv2.putText(frame,names[i]+" "+str(scores[i]),(int(bboxes[i][0]), int(bboxes[i][1])),0, 0.4, (255,255,255),1)
        
        
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame