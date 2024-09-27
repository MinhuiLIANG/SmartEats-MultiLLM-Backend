# from gevent import monkey
# monkey.patch_all()

# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# from gevent.pywsgi import WSGIServer
# from multiprocessing import cpu_count, Process
import sys

sys.path.append("..")
import fixedSentences
from DAO import dbops
from Components import enddetector
from Components import endtip


# app = Flask(__name__)
# cors = CORS(app)

# uid = "asdkhasd"
# @app.route('/endtwo', methods=['POST', 'GET'])
def EndTwo(uid):
    res = 'Enjoy your meal!'
    sent = 'Remember to eat healthy!'
    status = enddetector.end_interface(uid=uid)

    if 'yes' in status:
        dbops.upaccscnd(uid, "True")
        res = fixedSentences.prefixes["end2y"]

    if 'no' in status:
        dbops.upaccscnd(uid, "False")
        res = fixedSentences.prefixes["end2n"]

    tip = endtip.getips(uid)
    sent = res + '\n\nAnd, ' + tip

    dbops.upconversation_b(uid, sent)
    return {'endtwo': sent}

# def run(MULTI_PROCESS):
#  if MULTI_PROCESS == False:
#    WSGIServer(('0.0.0.0', 5000), app).serve_forever()


# if __name__ == "__main__":
#  run(False)
