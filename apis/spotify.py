import soundcloud
import requests as re
import base64

class Spotify:
    def __init__(self):
        self.token=self.getToke()
    
    def getToke(self):
        client_id='1f8980f1bf0240b2b49526e54bc84be8'
        client_secret='06a444c6af544d87adb23a61f322fb13'
        url='https://accounts.spotify.com/api/token'

        data=re.post(url,{
        'grant_type':'client_credentials',
        },auth=(client_id,client_secret)
        )
        token=data.json().get('access_token')

        return token
        
    def getMusic(self,album_id,number):
        url='https://api.spotify.com/v1/albums/'+album_id+'/tracks'
        res=re.get(url,params={
            'limit':1,
            'offset':number-1,
        },headers={
            'Authorization': 'Bearer '+self.token
        })
        
        res=res.json()

        items=res.get('items')
        music_url=items[0].get('preview_url')
        music_name=items[0].get('name')
        artist_name=items[0].get('artists')[0].get('name')

        items={
            "music_name":music_name,
            "artist_name":artist_name,
            "preview_url":music_url
        }
        return items
        
if __name__=='__main__':
    spotify=Spotify()
    spotify.getMusic('2G4AUqfwxcV1UdQjm2ouYr',9)