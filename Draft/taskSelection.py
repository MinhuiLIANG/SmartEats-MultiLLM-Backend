import random
#need to be stored in database
tasks = {"emotion":1,"hungerlevel":1,"limitation":0,"eatinggoal":0}

def chooseTask():
    taskAvailable = []
    for key in tasks:
        if tasks[key] == 0:
            taskAvailable.append(key)
            
    if len(taskAvailable) != 0:
        random.shuffle(taskAvailable)
        return taskAvailable[0]
    if len(taskAvailable) == 0:
        return 'finished'
