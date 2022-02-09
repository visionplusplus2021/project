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


class Notification:
    def send_SMS(str_event,mobile_no,str_clause):

        if(str_event==""):
            str_event = "test"
        account_sid = "AC58a715a490b93e64e3ac4f456208e779"
        # Your Auth Token from twilio.com/console
        auth_token  = "72c91dddc262429c30244b12d6380673"

        client = Client(account_sid, auth_token)

        str_aircraft = "aaa"
        str_clause = "bbb"
        image = Notification.getImage()

        # try:
            # Choosing file to send
        session = ftplib.FTP('files.000webhost.com','team-eager',')R8gmT#SRvGIIT5(TU8t')
        filename = 'camera.jpg'
        filepath = 'web/assets/img/camera.jpg'
        with open(filepath, 'rb') as file:
            print ('Opened file')

            # Sending the file
            print('Sending file')
            session.storbinary('STOR public_html/surveillance/' + filename, file)
            print('Sent file')
        session.quit()
        # except:
        #     pass



        message = client.messages \
                .create(
                     body= "Event Detected \nClick http://127.0.0.1:8001/stream to review the event ",
                     from_='+19252699150',
                     media_url=['https://team-eager.000webhostapp.com/surveillance/camera.jpg'],
                     to= mobile_no
                 )

        print(message.sid)
    def getImage():
        import cv2
        vidcap = cv2.VideoCapture('http://127.0.0.1:8001/stream')
        success,image = vidcap.read()
        cv2.imwrite("web/assets/img/camera.jpg", image) # save frame as JPEG file

        fp = open('web/assets/img/camera.jpg', 'rb')
        image = MIMEImage(fp.read())
        fp.close()

        return image
    def send_notification_email(str_event,EMAIL_ADDRESS,str_clause):


        # image_url = "http://127.0.0.1:8001/stream"




        message = MIMEMultipart()
        #
        # # http://127.0.0.1:8001/stream
        #
        # html = " test email"
        # from email.mime.image import MIMEImage
        # part = MIMEText(html, "html")
        # message.attach(part)
        #



        # Specify the  ID according to the img src in the HTML part
        image = Notification.getImage()
        image.add_header('Content-ID', '<camera>')
        message.attach(image)


        message["Subject"] = "Event Detected ("+str_event+")"
        text = message.as_string()




        port = 587   # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "ssukreep@gmail.com"
        receiver_email = EMAIL_ADDRESS
        password = "dwbtuaavmubnygpi"
        #df_config = Notification.getEmailAddressConfig()
        # port = df_config.port.values[0] #587   # For starttls
        # smtp_server = df_config.host.values[0]  #"smtp.gmail.com"
        # sender_email = df_config.host_user.values[0] #"ssukreep@gmail.com"
        # receiver_email = EMAIL_ADDRESS
        # password = df_config.host_password.values[0] #"dwbtuaavmubnygpi"



        # message["From"] = sender_email
        # message["To"] = receiver_email


        context = ssl.create_default_context()
        with smtplib.SMTP('smtp.gmail.com', port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
