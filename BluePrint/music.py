from flask import Flask,request,jsonify,abort,Blueprint,make_response,Response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.spotify import Spotify
import io
music_api = Namespace('music', description='Music APIs')

spotify=Spotify()

@music_api.route('/')

class Chat(Resource):
    @music_api.doc(responses={200: 'Success', 404: 'Parameter is empty', 500: 'Server Error'})
    def get(self):
        #data=request.args

        music=Spotify()
        music=music.getMusic('2G4AUqfwxcV1UdQjm2ouYr',9)
        print(len(music))
        return Response(music,mimetype='text/plain',direct_passthrough=True)
        return make_response(jsonify(chat=music),200)
            
 

