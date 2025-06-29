from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
import time
import sys 
sys.path.append("..") 
import topicTreesm
from Controllers import IBInterface
from Controllers import PreCCInterface
from Controllers import upgradeCCInterface
from Controllers import PreferenceInterface
from Controllers import upgradeRecInterface
from Controllers import FBInterface
from Controllers import upgradeEndone
from Controllers import upgradeEndtwo
from Controllers import upgradeConInterface
from Controllers import addInterface
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
    pc_cnt = dbops.getpreround(uid)
    if topic == 'rec1':
        action = control
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'prechat' and pc_cnt < 6:
        action = '<keep>'
    elif topic == 'prechat':
        action = upgradeConInterface.controlInterface(uid=uid)
        if action != '<down>':
            action = '<down>'
    elif topic == 'chitchat' and cc_cnt > 13:
        action = '<down>'
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'chitchat' and cc_cnt < 10:
        action = upgradeConInterface.controlInterface(uid=uid)
        if action != '<keep>':
            action = '<keep>'
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'chitchat':
        action = upgradeConInterface.controlInterface(uid=uid)
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'icebreak':
        action = '<down>'
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    else:
        action = '<down>'
        print('{tp} & {ac}'.format(tp=topic,ac=action))

    nxttopic = topicTreesm.movepter(topic, action)
    dbops.uplasttopic(uid, topic)
    dbops.uptopic(uid, nxttopic)
    
    topic = dbops.gettopic(uid)
    
    bot = 'emmmm'
    #action = '<down>'
    if topic == 'icebreak':
        dbops.uptopic(uid, 'prechat')
        topic = 'chitchat'
        #bot = IBInterface.IBInterface()['icebreak']
        #print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
    if topic == 'prechat':
        laststage = dbops.getlasttopic(uid)
        stime = time.time()
        bot = PreCCInterface.CCInterface(uid=uid, laststage=laststage)['prechitchat']
        etime = time.time()
        rtime = etime - stime
        dbops.upinfoctime(uid, rtime)
        print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
        pc_cnt = dbops.getpreround(uid)
        pc_cnt = pc_cnt + 1
        dbops.uppreround(uid, pc_cnt)
    if topic == 'chitchat':
        laststage = dbops.getlasttopic(uid)
        stime = time.time()
        bot = upgradeCCInterface.CCInterface(uid=uid, laststage=laststage)['chitchat']
        etime = time.time()
        rtime = etime - stime
        dbops.upinfoctime(uid, rtime)
        print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
        cc_cnt = dbops.getround(uid)
        cc_cnt = cc_cnt + 1
        dbops.upround(uid, cc_cnt)
    if topic == 'add':
        stime = time.time()
        bot = addInterface.AddInterface(uid=uid)['add']
        etime = time.time()
        rtime = etime - stime
        dbops.upinfoctime(uid, rtime)
        print('Avery: ', bot)
        #user = input("user: ")
        #dbops.upconversation_u(uid, user)
    if topic == 'rec1':
        stimereco = time.time()
        res = upgradeRecInterface.RecInterface('one',uid)
        etimereco = time.time()
        rtimereco = etimereco - stimereco
        dbops.uprectime(uid, rtimereco)
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
        stimerect = time.time()
        res = upgradeRecInterface.RecInterface('two',uid)
        etimerect = time.time()
        rtimerect = etimerect - stimerect
        dbops.uprectime(uid, rtimerect)
        
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
        bot = upgradeEndone.EndOne(uid=uid)['endone']
    if topic == 'end2':
        bot = upgradeEndtwo.EndTwo(uid=uid)['endtwo']
        print('Avery: ', bot)
        #end = True
    
    return {"chatbot":bot}

