from flask import Flask,request,jsonify,abort,Blueprint,make_response,Response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.spotify import Spotify
from apis.emotion_classfication_model import emotion_analysis
from apis.db import db
import random
import base64
music_api = Namespace('music', description='Music APIs')
# model=emotion_analysis('./models/emotion_classfication.h5',50432)
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
    @music_api.doc(responses={200: 'Success', 500: 'Server Error'}, params={'emotion':'sad'})
    def get(self):
        happy_musics=[]
        mad_musics=[]
        sad_musics=[]
        data=request.args
        emotion=data.get('emotion')
        
        for i in music_db.find(sort=[( "like", -1 )]):
            del i['_id']
            if i['emotion']=='sad':
                d={'music_name':i['name'],'view':i['view'],'artist_name':i['artist_name'],'cover_img':i['cover_img'],'preview_url':i['preview_url'],'like':i['like']}               
                sad_musics.append(d)
            elif i['emotion']=='mad':
                d={'music_name':i['name'],'view':i['view'],'artist_name':i['artist_name'],'cover_img':i['cover_img'],'preview_url':i['preview_url'],'like':i['like']}
                mad_musics.append(d)
            elif i['emotion']=='happy':
                d={'music_name':i['name'],'view':i['view'],'artist_name':i['artist_name'],'cover_img':i['cover_img'],'preview_url':i['preview_url'],'like':i['like']}
                happy_musics.append(d)
        if emotion=="sad":
            items={"musics":sad_musics}
        elif emotion=="mad":
            items={"musics":mad_musics}
        elif emotion=="happy":
            items={"musics":happy_musics}
        else: return make_response({"message":"there is not emotion"},404)
        # items={
        #     'happy_musics':happy_musics,'mad_musics':mad_musics,'sad_musics':sad_musics,
        # }
        return make_response(items,200)

@music_api.route('/like')      
class Like(Resource):
    @music_api.doc(responses={200: 'Success', 500: 'Server Error'}, params={'title':"Rollin'"})
    def get(self):
        data=request.args
        title=data.get('title')
        if title==None:
            return make_response({'message':'title is empty'},400)
        for i in music_db.find({'name':title}):
            i['like']+=1
            music_db.replace_one({"_id":i['_id']},i)      
            return make_response({'message':'success'},200)
        return make_response({'message':'title is wrong'},400)

@music_api.route('/music_insert')      
class Music_insert(Resource):
    @music_api.doc(responses={200: 'Success', 500: 'Server Error'}, params={'pw':'pw','music_key':'music_key','track_num':'track_num','emotion':'emotion'})
    def get(self):
        data=request.args
        pw=data.get('pw')
        if base64.b64encode(pw.encode('euc-kr'))!=b'YWxzd25zMDIyMQ==':
            return make_response({'message':'wrong password'},400)

        music_key=data.get('music_key')
        emotion=data.get('emotion')
        track_num=data.get('track_num')

        if not (emotion=='sad' or emotion=='happy' or emotion=='mad'):
            return make_response({'message':'emotion is wrong'},400)
        
        try:

            track_num=int(track_num)
            music=Spotify()
            items=music.getMusic(music_key,track_num)
        except:
            return make_response({'message':'param is wrong'},400)
            
        
        name=items['music_name']
        artist_name=items['artist_name']
        cover_img=items['cover_img']
        preview_url=items['preview_url']
        music_db.insert({'name':name,'artist_name':artist_name,'cover_img':cover_img,'music_key':music_key,'track_num':track_num,'emotion':emotion, 'hate':0,'view':0,'like':0,'preview_url':preview_url})
        
        return make_response({'message':'succes'},200)
    

