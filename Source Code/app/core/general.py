class General:
    def __init__(self):
        
        self.str_event = "Jaywalking"


    def getColor(self,index):
        color = ((255,0,0),(0,255,0),(0,0,255),(255,215,0),(255,0,255),(255,128,0))

        return color[index]