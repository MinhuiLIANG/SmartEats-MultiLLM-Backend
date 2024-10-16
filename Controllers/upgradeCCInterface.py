# from gevent import monkey
# monkey.patch_all()

# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
import openai
# from gevent.pywsgi import WSGIServer
# from multiprocessing import cpu_count, Process
import sys
import concurrent.futures

sys.path.append("..")
from Upgrades import questionasking
from Components import paraphraser
from Components import upgradeSlotFiller
from Components import addslot
from Components import adddislikeslot
from Components import LTMslot
from Components import preSlotFiller
from DAO import dbops

# app = Flask(__name__)
# cors = CORS(app)

# uid = 'asdkhasd'

# @app.route('/chatter', methods=['POST', 'GET'])
'''
def CCInterface():
    #shots, task = shotsCreator4chit.shots_interface()
    #meta = dbops.getlastround(uid)
    #lst = meta.split('user: ')
    #Avery = lst[0].replace('chatbot: ','')
    #user = lst[1]

    #conv = 'Avery: ' + str(Avery) + '\n' + 'User: ' + str(user)
    slotFiller.profile_editor()

    res = chitchatter.chatter_interface()
    #res_paraed = paraphraser.para_interface(res)
    dbops.upconversation_b(uid, res)
    return {"chitchat":res}
'''


def CCInterface(uid, laststage):
    if laststage != 'chitchat':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the first function for execution
            executor.submit(preSlotFiller.profile_editor, uid)
            # Submit the second function for execution
            chatter_interface_future = executor.submit(questionasking.chatter_interface, uid)

            # Wait for both functions to complete
            chatter_interface_result = chatter_interface_future.result()

            # Perform any necessary operations with the results

            # Update the conversation in the database
            dbops.upconversation_b(uid, chatter_interface_result)

            # Return the response
            return {"chitchat": chatter_interface_result}
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the first function for execution
            executor.submit(upgradeSlotFiller.profile_editor, uid)
            executor.submit(addslot.preslot_interface, uid)
            executor.submit(adddislikeslot.disslot_interface, uid)
            executor.submit(LTMslot.LTMslot_interface, uid)
            # Submit the second function for execution
            chatter_interface_future = executor.submit(questionasking.chatter_interface, uid)

            # Wait for both functions to complete
            chatter_interface_result = chatter_interface_future.result()

            # Perform any necessary operations with the results

            # Update the conversation in the database
            dbops.upconversation_b(uid, chatter_interface_result)

            # Return the response
            return {"chitchat": chatter_interface_result}

# def run(MULTI_PROCESS):
#  if MULTI_PROCESS == False:
#    WSGIServer(('0.0.0.0', 5000), app).serve_forever()


# if __name__ == "__main__":
#  run(False)