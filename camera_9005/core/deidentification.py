# import the necessary packages
import cv2

class Deidentification:
    def __init__(self, src_plate_cascade, src_face_cascade, name="Deidentification"):
        # cascade classifiers
        self.plate_cascade = cv2.CascadeClassifier(src_plate_cascade)
        self.face_cascade = cv2.CascadeClassifier(src_face_cascade)
        # initialize the thread name
        self.name = name

    def detect_plate(self,img):
        plate_img = img.copy()
        roi = img.copy()
        plate = self.plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 15) # detects car plates.
        for (x,y,w,h) in plate:
            roi1 = roi[y:y+h, x:x+w, :] # extracting the Region of Interest of license plate for blurring.
            blur = cv2.blur(roi1, ksize=(30,30)) # performing blur operation
            plate_img[y:y+h, x:x+w, :] = blur # replace the original license plate with the blurred one.
            cv2.rectangle(plate_img, (x,y), (x+w, y+h), (51,51,255), 3) # draw rectangles around the edges.
        return plate_img

    def detect_face(self,img):
        face_img = img.copy()
        roi = img.copy()
        plate = self.face_cascade.detectMultiScale(face_img, scaleFactor = 1.2, minNeighbors = 15) # detects car plates.
        for (x,y,w,h) in plate:
            roi1 = roi[y:y+h, x:x+w, :] # extracting the Region of Interest of face for blurring.
            blur = cv2.blur(roi1, ksize=(30,30)) # performing blur operation
            face_img[y:y+h, x:x+w, :] = blur # replace the original face with the blurred one.
            cv2.rectangle(face_img, (x,y), (x+w, y+h), (51,51,255), 3) # draw rectangles around the edges.
        return face_img