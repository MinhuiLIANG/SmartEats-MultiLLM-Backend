from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
from DAO import dbops


def proidapi():
    user_request = request.get_json()
    
    uid_ = user_request.get("uid")
    print('**uid_**:',uid_)
    proid = user_request.get("proid")
    surveytime = user_request.get("surveytime")
    uid = session.get('uid')
    
    if uid == None:
        uid = uid_.replace('@','').replace('.','')
    
    print('uid',uid)
    
    dbops.upproid(uid=uid, proid=proid)
    dbops.upsurveytime(uid=uid, surveytime=surveytime)
    return {"status":'OK'}
