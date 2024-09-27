from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import openai
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
from Controllers import SentInterface


def SentimentInterface():
    user_request = request.get_json()
    uid_ = user_request.get("uid")
    print('**uid_**:',uid_)
    uid = session.get('uid')
    if uid == None:
        uid = uid_.replace('@','').replace('.','')
    
    res = SentInterface.SentInterface(uid=uid)
    print('sentiment: ', res)
    return res
