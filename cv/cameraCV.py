import numpy as np
import cv2
from keras.preprocessing import image
from keras.models import model_from_json, load_model
from socket import *
import sys, os, time, json, hashlib, base64
import face_recognition

cvSocket = None
holdingArray = []
nameArray = []
user = "Unknown"

def runCV():
	global cvSocket, holdingArray
	face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt.xml')
	emotion_model = model_from_json(open('models/facial_expression_model_structure.json', 'r').read())
	emotion_model.load_weights('models/facial_expression_model_weights.h5')
	emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
	face_recognizer = face_recognition.setup()

	cap = cv2.VideoCapture(0)
	people = {0:"Raghav", 1:"Varun", 2:"Shivam", 3:"Akhila"}
	counter = 0

	cvSocket = socket(AF_INET, SOCK_DGRAM)
	cvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	cvSocket.bind((gethostbyname(gethostname()), 8001))

	while(True):
		# take frame, rescale, detect face
		ret, img = cap.read()
		img = cv2.resize(img, (640, 360))
		img = img[0:308,:]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x,y,w,h) in faces:
			if w > 100: #trick: ignore small faces
				cv2.rectangle(img,(x,y),(x+w,y+h),(64,64,64),2) #highlight detected face
				detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
				detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
				detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

				name_pred = face_recognition.predict(detected_face, face_recognizer)
				name = (people[name_pred[0]])
				if len(nameArray) < 10:
					nameArray.append(name)
				else:
					del nameArray[0]
					nameArray.append(name)

				counter += 1
				face_pixels = image.img_to_array(detected_face)
				face_pixels = np.expand_dims(face_pixels, axis = 0)
				face_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

				emotion_preds = emotion_model.predict(face_pixels) #store probabilities of 7 expressions

				#background of expression list
				overlay = img.copy()
				opacity = 0.4
				cv2.rectangle(img,(x+w+10,y-25),(x+w+150,y+115),(64,64,64),cv2.FILLED)
				cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)

				#connect face and expressions
				#TODO Name on top of emotions
				#cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
				cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
				cv2.line(img,(x+w,y-20),(x+w+10,y-20),(255,255,255),1)

				emotionArr = []
				for i in range(len(emotion_preds[0])):
					emotionArr.append((emotions[i], round(emotion_preds[0][i]*100, 2)))
					emotion = "%s %s%s" % (emotions[i], round(emotion_preds[0][i]*100, 2), '%')
					color = (255,255,255)
					cv2.putText(img, emotion, (int(x+w+15), int(y-12+i*20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
				emotion = max(emotionArr, key=lambda item:item[1])[0]
				# serverSendFunction(emotion)
				# print(emotion)
				if len(holdingArray) < 10:
					holdingArray.append(emotion)
				else:
					del holdingArray[0]
					holdingArray.append(emotion)

				print(holdingArray)

				maxEmotion = mostFrequent(holdingArray)
				user = mostFrequent(nameArray)
				strWithUser = maxEmotion + "," + user
				cvSocket.sendto(strWithUser.encode(), ('127.0.0.1', 8003))

		cv2.imshow('img',img)
		if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
			break
		# time.sleep(0.5)

	cap.release()
	cv2.destroyAllWindows()


def mostFrequent(emotions):
	n = len(emotions)
	arr = sorted(emotions)
	max_count = 1; res = arr[0]; curr_count = 1

	for i in range(1, n):
		if (arr[i] == arr[i - 1]):
			curr_count += 1
		else:
			if (curr_count > max_count):
				max_count = curr_count
				res = arr[i - 1]
			curr_count = 1

	if (curr_count > max_count):
		max_count = curr_count
		res = arr[n - 1]
	return res

if __name__ == '__main__':
	try:
		runCV()
	except KeyboardInterrupt:
		cvSocket.close()
		os._exit(1)
