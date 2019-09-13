import numpy as np
import cv2
from keras.preprocessing import image
from keras.models import model_from_json
import os

face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt.xml')


cap = cv2.VideoCapture(0)

folder_number = 0
person = ""
images_to_take = 150

counter = 0
while(counter < images_to_take):
	# take frame, rescale, detect face
	ret, img = cap.read()
	img = cv2.resize(img, (640, 360))
	img = img[0:308,:]
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		if w > 50: #trick: ignore small faces
			cv2.rectangle(img,(x,y),(x+w,y+h),(64,64,64),2) #highlight detected face
			detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
			detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
			detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
			os.mkdir("training-data/" + str(folder_number))
			cv2.imwrite( "training-data/" + str(folder_number) + "/" + person + "_" + str(counter) + ".jpg", detected_face );
			counter += 1

	cv2.imshow('img',img)
	if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
		break

cap.release()
cv2.destroyAllWindows()
