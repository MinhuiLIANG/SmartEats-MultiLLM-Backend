#from gevent import monkey
#monkey.patch_all()

#from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
import openai
#from gevent.pywsgi import WSGIServer
#from multiprocessing import cpu_count, Process
import sys
sys.path.append("..")
from Components import para4cus

def PaInterface(persona, style, cha):
    res = para4cus.para_cus(persona, style, cha)
    #res_paraed = paraphraser.para_interface(res)
    return res
