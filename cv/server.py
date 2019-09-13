from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import random
import requests

app = Flask(__name__)
api = Api(app)

USERS = {
    0: {'user': 'Raghav',
          'emotion': '',
          'playlists':
            {
                'happy': [],

                'sad': [],

                'angry': []
            }
         },

    1: {'user': 'Varun',
          'emotion': '',
          'playlists':
            {
                'happy': [],

                'sad': [],

                'angry': []
            }
         },

    2: {'user': 'Shivam',
          'emotion': '',
          'playlists':
            {
                'happy': [],

                'sad': [],

                'angry': []
            }
         },

    3: {'user': 'Akhila',
          'emotion': '',
          'playlists':
            {
                'happy': [],

                'sad': [],

                'angry': []
            }
         }
}


def abort_if_user_doesnt_exist(user_id):
    if user_id not in USERS:
        abort(404, message="user {} doesn't exist".format(USERS[user_id].user))

class User(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        return USERS.get(user_id)

    def put(self, user_id):
        args = parser.parse_args()
        emotion = {'emotion': args['emotion']}
        USERS[user_id]['emotion'] = emotion
        requests.post("http://localhost:3000/emotion", data=emotion)
        return emotion, 201

class Users(Resource):
    def get(self):
        return USERS

class Playlist(Resource):
    def get(self,user_id):
        user = USERS.get('user_id')
        emotion = user.get('emotion')
        playlist = user.get('playlists').get(emotion)
        return {'playlist': playlist}

class Song(Resource):
    def get(self,user_id):
        user = USERS.get('user_id')
        emotion = user.get('emotion')
        playlist = user.get('playlists').get(emotion)
        return {'song': random.choice(playlist)}

##
## Actually setup the Api resource routing here
##
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(Playlist, '/users/<int:user_id>/playlist')
api.add_resource(Song, '/users/<int:user_id>/playlist/song')

if __name__ == '__main__':
    app.run(debug=True)
