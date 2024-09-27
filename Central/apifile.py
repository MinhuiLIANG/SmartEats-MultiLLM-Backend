from gevent import monkey
monkey.patch_all()

from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process

from apilayer import cen_api
from ibfir import IBInterface
from senti import SentimentInterface
from hometran import homeapi
from bottran import botapi
from endtran import endapi
from proidtran import proidapi
from custran import cusapi

app = Flask(__name__)
#CORS(app, origins='https://minhuiliang.github.io', supports_credentials=True)

app.config["SECRET_KEY"] = 'asdbjbaskfajsdladas'

app.add_url_rule('/home', view_func=homeapi, methods=['POST', 'GET'])
app.add_url_rule('/back', view_func=cen_api, methods=['POST', 'GET'])
app.add_url_rule('/icebreak', view_func=IBInterface, methods=['POST', 'GET'])
app.add_url_rule('/cus', view_func=cusapi, methods=['POST', 'GET'])
app.add_url_rule('/bot', view_func=botapi, methods=['POST', 'GET'])
app.add_url_rule('/senti', view_func=SentimentInterface, methods=['POST', 'GET'])
app.add_url_rule('/end', view_func=endapi, methods=['POST', 'GET'])
app.add_url_rule('/proid', view_func=proidapi, methods=['POST', 'GET'])

http_server = WSGIServer(('0.0.0.0', 8080), app, log=None)
http_server.start()

def serve_forever():
    http_server.start_accepting()
    http_server._stop_event.wait()


if __name__ == "__main__":
    for i in range(cpu_count()*2):
        p = Process(target=serve_forever)
        p.start()
