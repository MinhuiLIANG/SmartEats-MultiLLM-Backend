from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
from DAO import dbops


#uid = 'asdkhasd'
def homeapi():
    #dbops.adduser(uid)
    user_request = request.get_json()
    email = user_request.get("email")
    
    session['uid'] = email.replace('@','').replace('.','')
    uid = email.replace('@','').replace('.','')

    dbops.addSmartEats(uid)

    dbops.upemail(uid, email)

    return {"status":'OK'}