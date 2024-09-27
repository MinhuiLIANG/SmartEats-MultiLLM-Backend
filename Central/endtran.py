from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys

sys.path.append("..")
from DAO import dbops


# uid = 'asdkhasd'
def endapi():
    user_request = request.get_json()
    uid_ = user_request.get("uid")
    print('**uid_**:', uid_)
    acca = user_request.get("acca")
    expa = user_request.get("expa")
    expb = user_request.get("expb")
    expc = user_request.get("expc")
    intera = user_request.get("intera")
    usefa = user_request.get("usefa")
    usefb = user_request.get("usefb")
    trusta = user_request.get("trusta")
    trustb = user_request.get("trustb")
    eata = user_request.get("eata")
    useia = user_request.get("useia")
    useib = user_request.get("useib")
    useic = user_request.get("useic")
    quaa = user_request.get("quaa")
    ada = user_request.get("ada")
    adb = user_request.get("adb")
    cusa = user_request.get("cusa")
    cusb = user_request.get("cusb")
    cusc = user_request.get("cusc")
    edul = user_request.get("edul")
    workf = user_request.get("workf")
    race = user_request.get("race")
    hper = user_request.get("hper")
    feedback = user_request.get("feedback")
    extra = user_request.get("extra")

    uid = session.get('uid')
    if uid == None:
        uid = uid_.replace('@', '').replace('.', '')

    dbops.upacca(uid, acca)
    dbops.upexpa(uid, expa)
    dbops.upexpb(uid, expb)
    dbops.upexpc(uid, expc)
    dbops.upintera(uid, intera)
    dbops.upusefa(uid, usefa)
    dbops.upusefb(uid, usefb)
    dbops.uptrusta(uid, trusta)
    dbops.uptrustb(uid, trustb)
    dbops.upeata(uid, eata)
    dbops.upuseria(uid, useia)
    dbops.upuserib(uid, useib)
    dbops.upuseric(uid, useic)
    dbops.upquaa(uid, quaa)
    dbops.upada(uid, ada)
    dbops.upadb(uid, adb)
    dbops.upedu(uid, edul)
    dbops.upwork(uid, workf)
    dbops.uprace(uid, race)
    dbops.uphper(uid, hper)
    dbops.upfeedback(uid, feedback)
    dbops.upextra(uid, extra)
    dbops.upcusa(uid, cusa)
    dbops.upcusb(uid, cusb)
    dbops.upcusc(uid, cusc)
    return {"status": 'OK'}
