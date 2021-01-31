from flask import Flask
from flask_cors import  CORS
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from BluePrint import chatbot
from flask_restplus import Resource, Api

app = Flask(__name__)


CORS(app)
api=Api(app)
api.add_namespace(chatbot.chatbot_api,'/chatbot')


if __name__=='__main__':
    #app.run(host='0.0.0.0',port=3000) 
    app.run(host='0.0.0.0',port=80, debug=True) 

