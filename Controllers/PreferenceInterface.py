#from gevent import monkey
#monkey.patch_all()

#from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
#from gevent.pywsgi import WSGIServer
#from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
import fixedSentences
from Components import slotFiller
from Components import preference
from DAO import dbops

#app = Flask(__name__)
#cors = CORS(app)

#uid = 'asdkhasd'
#@app.route('/pre', methods=['POST', 'GET'])
def PreferInterface(uid):
    slotFiller.profile_editor(uid=uid)
    res = fixedSentences.prefixes["prefb"]
    upres = preference.pref_interface(uid=uid) + '\n\n' + res
    dbops.upconversation_b(uid, upres)
    return {'pre':upres}



#def run(MULTI_PROCESS):
#  if MULTI_PROCESS == False:
#    WSGIServer(('0.0.0.0', 5000), app).serve_forever()


#if __name__ == "__main__":
#  run(False)
