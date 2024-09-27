#from gevent import monkey
#monkey.patch_all()

#from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
import openai
#from gevent.pywsgi import WSGIServer
#from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
from Components import paraphraser
from Components import iceBreaker
from DAO import dbops

#app = Flask(__name__)
#cors = CORS(app)

uid = 'asdkhasd'

#@app.route('/icebreak', methods=['POST', 'GET'])
def IBInterface():
    res = iceBreaker.iceBreak_interface()
    #res_paraed = paraphraser.para_interface(res)
    dbops.upconversation_b(uid, res)
    return {"icebreak":res}


#def run(MULTI_PROCESS):
#  if MULTI_PROCESS == False:
#    WSGIServer(('0.0.0.0', 5000), app).serve_forever()


#if __name__ == "__main__":
#  run(False)
