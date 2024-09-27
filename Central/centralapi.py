import sys 
sys.path.append("..") 
import topicTree
from Controllers import IBInterface
from Controllers import CCInterface
from Controllers import PreferenceInterface
from Controllers import RecInterface
from Controllers import EndInterfaceTwo
from Controllers import ControlInterface
from DAO import dbops

uid = 'asdkhasd'
end = False
cc_cnt = 0
while end == False:
    topic = dbops.gettopic(uid)
    if topic == 'icebreak':
        bot = IBInterface.IBInterface()['icebreak']
        print('Avery: ', bot)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
    if topic == 'chitchat':
        bot = CCInterface.CCInterface()['chitchat']
        print('Avery: ', bot)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
        cc_cnt = cc_cnt + 1
    if topic == 'preference':
        bot = PreferenceInterface.PreferInterface()['pre']
        print('Avery: ', bot)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
    if topic == 'rec1':
        res = RecInterface.RecInterface('one')
        bot_prefix = res['prefix']
        bot_rec1 = res['rec1']
        bot_rec2 = res['rec2']
        bot_aftfix = res['afterfix']
        print('Avery: ', bot_prefix)
        print('Avery: ', bot_rec1)
        if bot_rec2 != 'none':
            print('Avery: ', bot_rec2)
        print('Avery: ', bot_aftfix)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
    if topic == 'rec2':
        res = RecInterface.RecInterface('two')
        bot_prefix = res['prefix']
        bot_rec1 = res['rec1']
        bot_rec2 = res['rec2']
        bot_aftfix = res['afterfix']
        print('Avery: ', bot_prefix)
        print('Avery: ', bot_rec1)
        if bot_rec2 != 'none':
            print('Avery: ', bot_rec2)
        print('Avery: ', bot_aftfix)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
    if topic == 'end2':
        bot = EndInterfaceTwo.EndTwo()['endtwo']
        print('Avery: ', bot)
        end = True
    
    if topic == 'rec1':
        action = ControlInterface.controlInterface(order='<right>')
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'chitchat' and cc_cnt > 8:
        action = ControlInterface.controlInterface(order='<down>')
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    elif topic == 'chitchat' and cc_cnt < 2:
        action = ControlInterface.controlInterface(order='<keep>')
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    else:
        action = ControlInterface.controlInterface(order='none')
        print('{tp} & {ac}'.format(tp=topic,ac=action))
    nxttopic = topicTree.movepter(topic, action)
    
    dbops.uptopic(uid, nxttopic)