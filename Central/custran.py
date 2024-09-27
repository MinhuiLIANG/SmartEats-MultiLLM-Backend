from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys

sys.path.append("..")
from Controllers import ParaInterface


# uid = 'asdkhasd'
def cusapi():
    user_request = request.get_json()

    uid_ = user_request.get("uid")
    print('**uid_**:', uid_)
    persona = user_request.get("persona")
    style = user_request.get("style")
    cha = user_request.get("cha")
    uid = session.get('uid')

    if uid == None:
        uid = uid_.replace('@', '').replace('.', '')

    sentence = ParaInterface.PaInterface(persona, style, cha)

    return {"sentence": sentence}
