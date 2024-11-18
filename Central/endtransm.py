from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys

sys.path.append("..")
from DAO import dbops


# uid = 'asdkhasd'
def endsmapi():
    user_request = request.get_json()
    uid_ = user_request.get("userId")
    print('**uid_**:', uid_)

    resNuturalness = user_request.get("resNuturalness")
    resKnowledge = user_request.get("resKnowledge")
    recAcc = user_request.get("recAcc")
    recNovelo = user_request.get("recNovelo")
    recNovelt = user_request.get("recNovelt")
    recDiv = user_request.get("recDiv")
    adequacy = user_request.get("adequacy")
    sugQualityo = user_request.get("sugQualityo")
    sugQualityt = user_request.get("sugQualityt")
    expQualityo = user_request.get("expQualityo")
    expQualityt = user_request.get("expQualityt")
    imgQuality = user_request.get("imgQuality")
    eatIntent = user_request.get("eatIntent")
    satisfactiono = user_request.get("satisfactiono")
    satisfactiont = user_request.get("satisfactiont")
    useinentiona = user_request.get("useinentiona")
    useinentionb = user_request.get("useinentionb")
    useinentionc = user_request.get("useinentionc")
    trust = user_request.get("trust")
    time = user_request.get("time")
    edul = user_request.get("edul")
    workf = user_request.get("workf")
    race = user_request.get("race")
    feedback = user_request.get("feedback")
    extra = user_request.get("extra")

    uid = session.get('uid')
    if uid == None:
        uid = uid_.replace('@', '').replace('.', '')

    dbops.upresNuturalness(uid, resNuturalness)
    dbops.upresKnowledge(uid, resKnowledge)
    dbops.uprecAcc(uid, recAcc)
    dbops.uprecNovelo(uid, recNovelo)
    dbops.uprecNovelt(uid, recNovelt)
    dbops.uprecDiv(uid, recDiv)
    dbops.upadequacy(uid, adequacy)
    dbops.upsugQualityo(uid, sugQualityo)
    dbops.upsugQualityt(uid, sugQualityt)
    dbops.upexpQualityo(uid, expQualityo)
    dbops.upexpQualityt(uid, expQualityt)
    dbops.upimgQuality(uid, imgQuality)
    dbops.upeatIntent(uid, eatIntent)
    dbops.upsatisfactiono(uid, satisfactiono)
    dbops.upsatisfactiont(uid, satisfactiont)
    dbops.upuseinentiona(uid, useinentiona)
    dbops.upuseinentionb(uid, useinentionb)
    dbops.upuseinentionc(uid, useinentionc)
    dbops.uptrust(uid, trust)
    dbops.upedu(uid, edul)
    dbops.upwork(uid, workf)
    dbops.uprace(uid, race)
    dbops.upfeedback(uid, feedback)
    dbops.upextra(uid, extra)
    dbops.uptimeexp(uid, time)
    return {"status": 'OK'}
