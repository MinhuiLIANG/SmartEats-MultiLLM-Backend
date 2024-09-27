from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import sys 
sys.path.append("..") 
import topicTree
from Controllers import IBInterface
from Controllers import CCInterface
from Controllers import PreferenceInterface
from Controllers import RecInterface
from Controllers import FBInterface
from Controllers import EndInterfaceOne
from Controllers import EndInterfaceTwo
from Controllers import ControlInterface
from DAO import dbops

#uid = 'asdkhasd'
end = False

def cen_api():
    uid = session.get('uid')
    user_request = request.get_json()
    uid_ = user_request.get("uid")
    print('**uid_**:',uid_)
    user = user_request.get("user")
    control = user_request.get("control")
    cfood = user_request.get("choosefood")
    if uid == None:
        uid = uid_.replace('@','').replace('.','')
    
    topic = dbops.gettopic(uid)
    dbops.upconversation_u(uid, user)
    if cfood != 'none':
        dbops.upaccfood(uid, cfood)
    cc_cnt = dbops.getround(uid)
    if topic == 'rec1':
        action = ControlInterface.controlInterface(order=control,uid=uid)
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'chitchat' and cc_cnt > 8:
        action = ControlInterface.controlInterface(order='<down>',uid=uid)
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'chitchat' and cc_cnt < 6:
        action = ControlInterface.controlInterface(order='<keep>',uid=uid)
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    else:
        action = ControlInterface.controlInterface(order='none',uid=uid)
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    nxttopic = topicTree.movepter(topic, action)

    dbops.uptopic(uid, nxttopic)
    
    topic = dbops.gettopic(uid)
    
    bot = 'emmmm'
    #action = '<down>'
    if topic == 'icebreak':
        dbops.uptopic(uid, 'chitchat')
        topic = 'chitchat'
        #bot = IBInterface.IBInterface()['icebreak']
        #print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
    if topic == 'chitchat':
        bot = CCInterface.CCInterface(uid=uid)['chitchat']
        print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
        cc_cnt = dbops.getround(uid)
        cc_cnt = cc_cnt + 1
        dbops.upround(uid, cc_cnt)
    if topic == 'preference':
        bot = PreferenceInterface.PreferInterface(uid=uid)['pre']
        print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
    if topic == 'rec1':
        res = RecInterface.RecInterface('one',uid)
        bot_prefix = res['prefix']
        bot_food1 = res['food1']
        bot_rec1 = res['rec1']
        bot_img1 = res['img1']
        bot_food2 = res['food2']
        bot_rec2 = res['rec2']
        bot_img2 = res['img2']
        bot_aftfix = res['afterfix']
        print('Avery: ', bot_prefix)
        print('Avery: ', bot_rec1)
        if bot_rec2 != 'none':
            print('Avery: ', bot_rec2)
            bot = bot_food1 + '[CLS]' + bot_rec1 + '[CAT]' + bot_img1 + '[REC]' + bot_food2 + '[CLS]' + bot_rec2 + '[CAT]' + bot_img2
        if bot_rec2 == 'none':
            bot = bot_food1 + '[CLS]' + bot_rec1 + '[CAT]' + bot_img1
        print('Avery: ', bot_aftfix)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
    if topic == 'feedback':
        bot = FBInterface.FeedbackInterface(uid=uid)['fb']
        print('Avery: ', bot)
    if topic == 'rec2':
        res = RecInterface.RecInterface('two',uid)
        bot_prefix = res['prefix']
        bot_food1 = res['food1']
        bot_rec1 = res['rec1']
        bot_img1 = res['img1']
        bot_food2 = res['food2']
        bot_rec2 = res['rec2']
        bot_img2 = res['img2']
        bot_aftfix = res['afterfix']
        print('Avery: ', bot_prefix)
        print('Avery: ', bot_rec1)
        if bot_rec2 != 'none':
            print('Avery: ', bot_rec2)
            bot = bot_food1 + '[CLS]' + bot_rec1 + '[CAT]' + bot_img1 + '[REC]' + bot_food2 + '[CLS]' + bot_rec2 + '[CAT]' + bot_img2
        if bot_rec2 == 'none':
            bot = bot_food1 + '[CLS]' + bot_rec1 + '[CAT]' + bot_img1
        print('Avery: ', bot_aftfix)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
    if topic == 'end1':
        bot = EndInterfaceOne.EndOne(uid=uid)['endone']
    if topic == 'end2':
        bot = EndInterfaceTwo.EndTwo(uid=uid)['endtwo']
        print('Avery: ', bot)
        #end = True
    
    return {"chatbot":bot}

