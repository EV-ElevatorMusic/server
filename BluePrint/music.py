from flask import Flask,request,jsonify,abort,Blueprint,make_response,Response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.spotify import Spotify
from apis.emotion_classfication_model import emotion_analysis
from db import db

music_api = Namespace('music', description='Music APIs')
model=emotion_analysis('./models/emotion_classfication.h5',50432)
# spotify=Spotify()
music_db=db['music']
@music_api.route('/')

# 0:기쁨
# 1:분노
# 2:슬픔
class Chat(Resource):
    @music_api.doc(responses={200: 'Success', 404: 'Parameter is empty', 500: 'Server Error'}, params={'comment': '안녕'})
    def get(self):
        data=request.args
    
        comment=data.get('comment')
        if comment==None:
            return abort(404,"There is not comment")
        emotion=model.pred(comment)

        if emotion==0:
            music_list=music_db.find({'emotion':'happy'})
        elif emotion==1:
            music_list=music_db.find({'emotion':'mad'})
        elif emotion==2:
            music_list=music_db.find({'emotion':'sad'})
        print(type(music_list))
        
        music=Spotify()
        items=music.getMusic('2G4AUqfwxcV1UdQjm2ouYr',9)
        
        return make_response(items,200)
            
 

