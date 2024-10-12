# we need a tree bc let gpt maintain the topic content is too difficult, if it just maintains a pointer, then the action would be just <down> and <keep>
#it is much more simpler just like a intent detector.

ib = {'name':'icebreak','child1':'chitchat','child2':'none','parent':'none'}
cc = {'name':'chitchat','child1':'rec1','child2':'none','parent':'icebreak'}
r1 = {'name':'rec1','child1':'end1','child2':'feedback','parent':'chitchat'}
e1 = {'name':'end1','child1':'none','child2':'none','parent':'rec1'}
fb = {'name':'feedback','child1':'rec2','child2':'none','parent':'rec1'}
r2 = {'name':'rec2','child1':'end2','child2':'none','parent':'feedback'}
e2 = {'name':'end2','child1':'none','child2':'none','parent':'rec2'}

topic_tree = []
topic_tree.append(ib)
topic_tree.append(cc)
topic_tree.append(r1)
topic_tree.append(e1)
topic_tree.append(fb)
topic_tree.append(r2)
topic_tree.append(e2)

constraits = [('icebreak','down'),('chitchat','down'),('chitchat','keep'),('rec1','left'),('rec1','right'),('feedback','down'),('rec2','down')]

#currtopic: just finished, AKA last topic
def goDown(currtopic):
    nxttopic = 'none'
    if currtopic != 'rec1' and currtopic != 'end1' and currtopic != 'end2':
        for topic in topic_tree:
            if topic['name'] == currtopic:
                nxttopic = topic['child1']
                break
    return nxttopic

def goLeft(currtopic):
    nxttopic = 'none'
    if currtopic == 'rec1':
        nxttopic = r1['child1']
    return nxttopic
     
def goRight(currtopic):
    nxttopic = 'none'
    if currtopic == 'rec1':
        nxttopic = r1['child2']
    return nxttopic

def unpacking(res):
    act_unpacked = res.replace('<','').replace('>','').replace(' ','')
    return act_unpacked

def movepter(currentTopic, res):
    nxttopic = 'none'
    tagtmp = False
    #unpack
    action = unpacking(res)
    #constraint
    pair = (currentTopic, action)
    for item in constraits:
        if pair == item:
            tagtmp = True
            break
    if tagtmp == True:
        if action == 'keep':
            nxttopic = currentTopic
        if action == 'down':
            nxttopic = goDown(currentTopic)
        if action == 'left':
            nxttopic = goLeft(currentTopic)
        if action == 'right':
            nxttopic = goRight(currentTopic)
    else:
        #default
        if currentTopic == 'rec1':
            nxttopic = goLeft(currentTopic)
        else:
            nxttopic = goDown(currentTopic)
    
    return nxttopic