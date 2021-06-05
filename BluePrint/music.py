from flask import Flask,request,jsonify,abort,Blueprint,make_response,Response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.spotify import Spotify
from apis.emotion_classfication_model import emotion_analysis
import io
music_api = Namespace('music', description='Music APIs')
model=emotion_analysis('./models/emotion_classfication.h5',50432)
# spotify=Spotify()

@music_api.route('/')

class Chat(Resource):
    @chatbot_api.doc(responses={200: 'Success', 404: 'Parameter is empty', 500: 'Server Error'}, params={'comment': '안녕'})
    def get(self):
        data=request.args
    
        comment=data.get('comment')
        if comment==None:
            return abort(404,"There is not comment")
        print(model.pred(comment))
        music=Spotify()
        items=music.getMusic('2G4AUqfwxcV1UdQjm2ouYr',9)
        
        return make_response(items,200)
            
 

