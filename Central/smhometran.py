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
    gender = user_request.get("gender")
    age = user_request.get("age")
    height = user_request.get("height")
    weight = user_request.get("weight")
    location = user_request.get("location")
    
    contraindication = user_request.get("contraindication")
    healthconcern = user_request.get("healthconcern")
    
    session['uid'] = email.replace('@','').replace('.','')
    uid = email.replace('@','').replace('.','')

    dbops.addSmartEats(uid)

    dbops.upemail(uid, email)
    dbops.upgender(uid, gender)
    dbops.upage(uid, age)
    dbops.upheight(uid, height)
    dbops.upweight(uid, weight)
    dbops.uploc(uid, location)
    
    dbops.upcon(uid, contraindication)
    dbops.upconcern(uid, healthconcern)
    return {"status":'OK'}