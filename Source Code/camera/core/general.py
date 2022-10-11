import pymongo
from bson import  json_util
import json


class General:
    def __init__(self):
        
        self.str_event = "Jaywalking"


    def getColorLabel(self,index):
        color = ((255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(255,128,0),
                (139, 0, 0), (0, 100, 0),(0, 0, 139),(255,215,0),(255,0,255),(0,255,255))

        return color[index]

    def getColorDetect(self,index):
        color = ((0,0,255),(0,255,0),(153,51,0),(255,128,128),(0,0,128),(128,0,0),(255,204,0),(51,102,255),
                (204,153,255),(255,255,204),(255,153,0),(153,204,0) ,(0,102,204),(255,102,0),(153,204,255),
                (153,153,255) ,(255,0,255),(153,51,102),(255,0,0),(255,153,204),(51,153,102),(0,204,255),
                (255,204,153),(0,128,128) ,(0,255,255),(255,255,153),(128,0,128),(255,255,0))

        return color[index]
    
    def getColorTextDisplay(self,index):
        color = ((19,16,112),(13,88,28),(116,10,19),
                (15,103,108), (0, 100, 0),(0, 0, 139),(255,255,0),(255,0,255),(0,255,255))

        return color[index]

    
    def getDefaultCamera_byServer(self,server):

        URL = ""
        dbMain = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = pymongo.MongoClient(dbMain)
        db = client['city_of_oshawa']
        col = db['camera']

        results = col.find({ "server":server})
        json_data = json_util.dumps(results)
        j_data = json.loads(json_data)


        if(len(j_data) > 0):
            URL = j_data[0]["url"]

        return URL