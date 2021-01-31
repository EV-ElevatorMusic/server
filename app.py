from flask import Flask
import flask
from flask_cors import  CORS, cross_origin
from flask_restplus import Resource, Api

from BluePrint import chatbot
app = Flask(__name__)


CORS(app)
api=Api(app)
api.add_namespace(chatbot.chatbot_api,'/chatbot')


if __name__=='__main__':
    #app.run(host='0.0.0.0',port=3000) 
    app.run(host='0.0.0.0',port=3000, debug=True) 

