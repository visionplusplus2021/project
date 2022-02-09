from operator import xor
from absl import app
from twilio.rest import Client
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib, ssl
import requests
import shutil
import ftplib

import certifi
import pymongo

class Notification:
    def __init__(self):
        self.ca = certifi.where()
        self.dbMain = "mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(self.dbMain,tlsCAFile=self.ca)
        self.db = self.client['city_of_oshawa']
        self.str_event = "Jaywalking"
      

    def send_notification_SMS(self,video_name,image,str_event):

        account_sid = "AC58a715a490b93e64e3ac4f456208e779"
        # Your Auth Token from twilio.com/console
        auth_token  = "72c91dddc262429c30244b12d6380673"

        client = Client(account_sid, auth_token)

       
        image,path = Notification.getImage(image)

        # try:
            # Choosing file to send

        
        session = ftplib.FTP('files.000webhost.com','team-eager',')R8gmT#SRvGIIT5(TU8t')
        #session = ftplib.FTP('files.000webhost.com','teaching-city','#Q46IFuQT6cv5sDvB@83')
        filename = 'camera.jpg'
        
        filepath = path+"/camera.jpg"
        with open(filepath, 'rb') as file:
            print ('Opened file')

            # Sending the file
            print('Sending file')
            session.storbinary('STOR public_html/surveillance/' + filename, file)
            print('Sent file')
        session.quit()


        mycol = self.db["contact"]
        customers = mycol.find()

        for x in customers:
            if(str_event in (str(x["features_sms"]))):
                str_mobile = "+1"+x["mobile"]
            
                message = client.messages \
                        .create(
                            body= str_event+" is detected. \nPlease check the video name:'"+video_name+"' to review the event ",
                            from_='+19252699150',
                            media_url=['https://team-eager.000webhostapp.com/surveillance/camera.jpg'],
                            to= str_mobile
                    )

                print(message.sid)
    def getImage(image):
        import cv2
        import os

        

        APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
        path = APP_ROOT.replace("core","data")+"/img"
        cv2.imwrite(path+"/camera.jpg", image) # save frame as JPEG file

        fp = open(path+"/camera.jpg", 'rb')
        image = MIMEImage(fp.read())
        fp.close()

        return image,path

    def send_notification_email(self,video_name,image,str_event):


        # image_url = "http://127.0.0.1:8001/stream"


        

        message = MIMEMultipart()

        image,path = Notification.getImage(image)
        image.add_header('Content-ID', '<camera>')
        message.attach(image)


        message["Subject"] = str_event+" is detected ("+video_name+")"
        text = message.as_string()
        
        mycol = self.db["contact"]
        customers = mycol.find()
       
        for x in customers:
            
            if(str_event in (str(x["features_email"]))):
               
            
                port = 587   # For starttls
                smtp_server = "smtp.gmail.com"
                sender_email = "ssukreep@gmail.com"
                receiver_email = x["email"]#EMAIL_ADDRESS
                #password = "dwbtuaavmubnygpi"
                password = "ickrmhxfbedcwisj"
                context = ssl.create_default_context()
                with smtplib.SMTP('smtp.gmail.com', port) as server:
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)