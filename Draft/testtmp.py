import sys 
sys.path.append("..") 
import topicTree
from Controllers import IBInterface
from Controllers import CCInterface
from Controllers import PreferenceInterface
from Controllers import RecInterface
from Controllers import EndInterfaceTwo
from Components import controller
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
        tp = controller.controller('none')
        print('next topic:', tp)
    if topic == 'chitchat':
        bot = CCInterface.CCInterface()['chitchat']
        print('Avery: ', bot)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
        cc_cnt = cc_cnt + 1
        if cc_cnt < 4:
            tp = controller.controller('none')
        if cc_cnt >= 4:
            tp = controller.controller('<down>')
        print('next topic:', tp)
    if topic == 'preference':
        bot = PreferenceInterface.PreferInterface()['pre']
        print('Avery: ', bot)
        user = input("user: ")
        dbops.upconversation_u(uid, user)
        tp = controller.controller('none')
        print('next topic:', tp)
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
        tp = controller.controller('<right>')
        print('next topic:', tp)
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
        tp = controller.controller('none')
        print('next topic:', tp)
    if topic == 'end2':
        bot = EndInterfaceTwo.EndTwo()['endtwo']
        print('Avery: ', bot)
        end = True
    
    action = '<down>'
    if topic == 'rec1':
        action = '<right>'
    if topic == 'chitchat' and cc_cnt < 4:
        action = '<keep>'
    nxttopic = topicTree.movepter(topic, action)
    
    dbops.uptopic(uid, nxttopic)
    


