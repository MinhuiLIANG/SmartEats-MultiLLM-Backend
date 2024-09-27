#from gevent import monkey
#monkey.patch_all()

#from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
import openai
#from gevent.pywsgi import WSGIServer
#from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
from Components import postrec
import json
  
#app = Flask(__name__)
#cors = CORS(app)

#@app.route('/rec', methods=['POST', 'GET'])
def RecInterface(round,uid):
  #user_request = request.get_json()
  #round = user_request.get("round")
  #return recommender.rec_interface(round)
  return postrec.postrec_interface(round,uid)

#def run(MULTI_PROCESS):
#  if MULTI_PROCESS == False:
#    WSGIServer(('0.0.0.0', 5000), app).serve_forever()


#if __name__ == "__main__":
#  run(False)
