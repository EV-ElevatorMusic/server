from flask import Flask,request,jsonify,abort,Blueprint,make_response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.dialogflow import Dialogflow
from apis.train_torch import KoGPT2Chat
from apis.spotify import Spotify
from apis.emotion_classfication_model import emotion_analysis
from apis.db import db
import random
import base64

chatbot_api = Namespace('chatbot', description='Chatbot APIs')
path='models/model.ckpt'
model = KoGPT2Chat.load_from_checkpoint(path)
dialogflow=Dialogflow()

music_db=db['music']

@chatbot_api.route('/')

# class Chat(Resource):
#     @chatbot_api.doc(responses={200: 'Success', 404: 'Parameter is empty', 500: 'Server Error'}, params={'comment': '안녕'})
#     def get(self):
#         data=request.args
    
#         comment=data.get('comment')
#         print(comment)
#         if comment==None:
#             return abort(404,"There is not comment")
#         else:
#             chat=dialogflow.predict(comment)
#             if chat == None:
#                 dialogflow.refresh_token()
#                 chat=dialogflow.predict(comment)
#                 if chat==None:
#                     return abort(500,"error")
                
#             return make_response(jsonify(chat=chat),200)

class Chat(Resource):
    @chatbot_api.doc(responses={200: 'Success', 404: 'Parameter is empty', 500: 'Server Error'}, params={'comment': '안녕'})
    def get(self):
        keyword_fill=False
        data=request.args
        comment=data.get('comment')
        keyword=['기분 좋아','행복','안 좋아','속상','화나','짜증','기분 좋은','안 좋은','화나는']
        
        
        if comment==None:
            return abort(404,"There is not comment")
        comment=str(comment)
        
        for i in keyword:
            if comment.find(i)!=-1:
                keyword_fill=True
                break
        if keyword_fill:
            items=self.recommend_music(comment)
            return make_response(jsonify(responsetype='music',music=items),200)

        else:
            chat=model.chat(comment)        
            if chat==None:
                return abort(500,"error")
            return make_response(jsonify(responsetype='chat',chat=chat),200)
    def recommend_music(self,comment):
        emotion=model.pred(comment)

        if emotion==0:
            music_list=music_db.find({'emotion':'happy'})
        elif emotion==1:
            music_list=music_db.find({'emotion':'mad'})
        elif emotion==2:
            music_list=music_db.find({'emotion':'sad'})
        music_list=list(music_list)
        song=random.choice(music_list)
        key=song['music_key']
        track_num=song['track_num']
        song['view']+=1
        music_db.replace_one({"_id":song['_id']},song)

        music=Spotify()
        items=music.getMusic(key,track_num)
        return items