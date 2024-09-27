from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import openai
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
from Components import paraphraser
from Components import iceBreaker
import topicTree
from DAO import dbops

#uid = 'asdkhasd'

def IBInterface():
    user_request = request.get_json()
    uid_ = user_request.get("uid")
    print('**uid_**:',uid_)
    uid = session.get('uid')
    if uid == None:
        uid = uid_.replace('@','').replace('.','')
    
    res = iceBreaker.iceBreak_interface(uid=uid)
    #res_paraed = paraphraser.para_interface(res)
    dbops.upconversation_b(uid, res)
    #topic = dbops.gettopic(uid)
    #action = '<down>'
    #nxttopic = topicTree.movepter(topic, action)
    #dbops.uptopic(uid, nxttopic)
    return {"icebreak":res}
