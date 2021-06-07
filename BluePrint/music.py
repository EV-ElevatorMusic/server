from flask import Flask,request,jsonify,abort,Blueprint,make_response,Response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.spotify import Spotify
from apis.emotion_classfication_model import emotion_analysis
from apis.db import db
import random
import base64
music_api = Namespace('music', description='Music APIs')
model=emotion_analysis('./models/emotion_classfication.h5',50432)
# spotify=Spotify()
music_db=db['music']
# 0:기쁨
# 1:분노
# 2:슬픔

@music_api.route('/')
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
        music_list=list(music_list)
        song=random.choice(music_list)
        key=song['music_key']
        track_num=song['track_num']
        song['view']+=1
        music_db.replace_one({"_id":song['_id']},song)

        music=Spotify()
        items=music.getMusic(key,track_num)

        return make_response(items,200)

@music_api.route('/music_list')      
class Music_list(Resource):
    @music_api.doc(responses={200: 'Success', 500: 'Server Error'}, params={})
    def get(self):
        happy_musics=[]
        mad_musics=[]
        sad_musics=[]
        for i in music_db.find(sort=[( "view", 1 )]):
            del i['_id']
            if i['emotion']=='sad':
                d={'music_name':i['name'],'view':i['view']}               
                sad_musics.append(d)
            elif i['emotion']=='mad':
                d={'music_name':i['name'],'view':i['view']}
                mad_musics.append(d)
            elif i['emotion']=='happy':
                d={'music_name':i['name'],'view':i['view']}
                happy_musics.append(d)
        items={
            'happy_musics':happy_musics,'mad_musics':mad_musics,'sad_musics':sad_musics,'message':'succes'
        }
        return make_response(items,200)

@music_api.route('/music_insert')      
class Music_insert(Resource):
    @music_api.doc(responses={200: 'Success', 500: 'Server Error'}, params={'pw':'pw','music_key':'music_key','track_num':'track_num','emotion':'emotion'})
    def get(self):
        data=request.args
        pw=data.get('pw')
        if base64.b64encode(pw.encode('euc-kr'))!=b'YWxzd25zMDIyMQ==':
            return make_response({'message':'wrong password'},400)

        name=data.get('name')
        music_key=data.get('music_key')
        emotion=data.get('emotion')
        track_num=data.get('track_num')

        
        music_db.insert({'name':name,'music_key':music_key,'track_num':int(track_num),'emotion':emotion, 'view':0})
        
        return make_response({'message':'succes'},200)
    

