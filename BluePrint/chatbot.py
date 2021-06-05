from flask import Flask,request,jsonify,abort,Blueprint,make_response
# from .dialogflow import Dialogflow
from flask_restplus import Namespace,Resource
from apis.dialogflow import Dialogflow
from apis.train_torch import KoGPT2Chat
chatbot_api = Namespace('chatbot', description='Chatbot APIs')
path='models/model.ckpt'
model = KoGPT2Chat.load_from_checkpoint(path)
dialogflow=Dialogflow()

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
        data=request.args
    
        comment=data.get('comment')
        print(comment)
        if comment==None:
            return abort(404,"There is not comment")
        else:
            chat=model.chat(comment)
            # if chat == None:
            #     dialogflow.refresh_token()
            #     chat=dialogflow.predict(comment)
            #     if chat==None:
            #         return abort(500,"error")
            if chat==None:
                return abort(500,"error")
                
            return make_response(jsonify(chat=chat),200)
