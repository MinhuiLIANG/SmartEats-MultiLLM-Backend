#from gevent import monkey
#monkey.patch_all()

#from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
#from gevent.pywsgi import WSGIServer
#from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
import fixedSentences
from Components import upgradeSlotFiller
from Components import add
from DAO import dbops

#app = Flask(__name__)
#cors = CORS(app)

#uid = 'asdkhasd'
#@app.route('/pre', methods=['POST', 'GET'])
def AddInterface(uid):
    upgradeSlotFiller.profile_editor(uid=uid)
    res = fixedSentences.prefixes["add"]
    upres = add.add_interface(uid=uid) + '\n\n' + res
    dbops.upconversation_b(uid, upres)
    return {'add':upres}



#def run(MULTI_PROCESS):
#  if MULTI_PROCESS == False:
#    WSGIServer(('0.0.0.0', 5000), app).serve_forever()


#if __name__ == "__main__":
#  run(False)
