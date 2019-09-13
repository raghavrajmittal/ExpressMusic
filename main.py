from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, disconnect
from socket import *
import sys, os, time, json, hashlib, base64
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)
cvSocket = None

trueEmotion = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def my_event(msg):
    print(msg['data'])

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

def changeSong(message):
    msg = message.decode().split(",")
    emotion = msg[0]
    user = msg[1]
    print(emotion, user)

    global trueEmotion
    if (trueEmotion == emotion):
        return

    trueEmotion = emotion

    if emotion == 'happy':
        song = 'MOWDb2TBYDg'
    elif emotion == 'sad':
        song = 'd-diB65scQU'
    elif emotion == 'angry':
        song = 'Zv479MCnThA'
    elif emotion == 'disgust':
        song = 'jofNR_WkoCE'
    elif emotion == 'fear':
        song = '4V90AmXnguw'
    elif emotion == 'surprise':
        song = 'gkBvuhBBhvA'
    elif emotion == 'neutral':
        song = 'ymHBUyui_ws'
    else:
        song = 'ymHBUyui_ws'

    socketio.emit('message', {'emotion': emotion, 'user': user, 'song': song}, namespace='/test')

def startCVSocket():
    global cvSocket
    cvSocket = socket(AF_INET, SOCK_DGRAM)
    cvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cvSocket.bind(("127.0.0.1", 8003))
    while True:
        message, clientAddress = cvSocket.recvfrom(2048)
        changeSong(message)

if __name__ == '__main__':
    try:
        Thread(target=startCVSocket).start()
        socketio.run(app)
    except KeyboardInterrupt:
        cvSocket.close()
        os._exit(1)
