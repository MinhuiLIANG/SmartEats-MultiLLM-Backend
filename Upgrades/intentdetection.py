from openai import OpenAI
import random
import sys 
sys.path.append("..") 
from DAO import dbops

#uid = 'asdkhasd'
def intentdetection(uid):
    origintask = ['emotion', 'env', 'goal', 'his', 'hunger level', 'time limitation', 'preference', 'budget', 'social', 'culture', 'exercise']
    tasklst = dbops.gettasklst(uid)
    print('tasklist: ', tasklst)
    pretasks = dbops.getprevtasks(uid)
    print('prevtasklist: ', pretasks)

    conv = dbops.getwholeconversation(uid)

    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ','')
    user = lst[1]
    av = str(Avery)
    us = str(user)
    conversation = 'chatbot: ' + av + '\n' + 'user: ' + us

    lasttask = dbops.getlasttask(uid)
    print('last topic: ', lasttask)
    controllerprompt = ''
    avaitask = []
    if tasklst != 'finished':
      avaitask = tasklst
      avaitask.append(lasttask)
      controllerprompt = '''
      Definition of topics:
      <emotion>: asking about the user's recent emotion status
      <env>: asking about the user's daily dining environment, eating outside or cooking at home
      <goal>: asking about the user's dietary goal, if the user has any health aspects to be improved.
      <his>: asking about what foods the user usually have in daily lives.
      <hunger level>: asking about the user's eating habits, whether the user eat regularly or just eat when hungry
      <time limitation>: asking about how much time the user can spend for a meal
      <preference>: asking about the user's food or flavor preference
      <budget>: asking about the user's budget for meals, whether it is flexible or tight
      <social>: asking about the social environment when the user has meals, whether usually eating alone or with others
      <culture>: asking about the user's food culture
      <exercise>: asking about the user's exercise habit, whether the user often exercise or not
      
      [rest topics]-><{}>
      [last topic]-><{lasttask}>
      [conversation log]->
      <{conversation}>
      
      I am managing the flow of a conversation including various topics related to user's eating habits. The Definition of topics are listed at the beginning. [last topic] represents the topic just delivered in [conversation log] in the form of a question corresponding to it, [rest topics] represents the topics that are going to be asked, [conversation log] records how the [last topic] is delivered and the user's reaction to it. 
      In [conversation log], the topics are delivered to the user by asking corresponding questions relevant to the Definition of topics above. For instance, the chabot may deliver <culture> topic by asking 'By the way, do you have a preferred cuisine type or cooking style?'
      According to the [conversation log], I judge if the question corresponding to [last topic] were successfully asked and user was clear about it. If the question is (1) overlooked (chatbot did not ask any questions), (2) not relevant to [last topic] (chatbot asked a question not related to [last topic]), or (3) user ask for further elaboration for the question, I will output the value of [last topic] (in <>).
      If the [last topic] was successfully delivered, I *MUST NOT* deliver [last topic] again. Instead, I will output a certain topic *from [rest topics]* according to the user's message in [conversation log], which can make the conversation flow smooth, natural and coherent. In this case, the topic I select MUST from [rest topics].
      
      *Caution!*: I can *ONLY* select a topic from [rest topics] and [last topic]! I *MUST NOT* select any topic not belonging to [rest topics] or [last topic]! I will take the *Caution!* above very seriously.
      *KEEP IN MIND*: Here is an example of a WRONG output: 
      [rest topics]-><time limitation> 
      [last topic]-><hunger level>
      WRONG output: <goal>
      Above output is WRONG because <goal> is not from [rest topics] and [last topic]. In fact, any topics other than <time limitation> or <hunger level> is WRONG in this example!
      
      Looking at the instruction and example above, now I understand how to manage the conversation flow and select the appropriate topic.
      '''.format(", ".join(tasklst), lasttask=lasttask, conversation=conversation)
    else:
      controllerprompt = '''
      [asked topics]-><'emotion', 'env', 'goal', 'his', 'hunger level', 'time limitation', 'preference', 'budget', 'social', 'culture', 'exercise'>
      
      Definition of topics:
      <emotion>: asking about the user's recent emotion status
      <env>: asking about the user's daily dining environment, eating outside or cooking at home
      <goal>: asking about the user's dietary goal, if the user has any health aspects to be improved.
      <his>: asking about what foods the user usually have in daily lives.
      <hunger level>: asking about the user's eating habits, whether the user eat regularly or just eat when hungry
      <time limitation>: asking about how much time the user can spend for a meal
      <preference>: asking about the user's food or flavor preference
      <budget>: asking about the user's budget for meals, whether it is flexible or tight
      <social>: asking about the social environment when the user has meals, whether usually eating alone or with others
      <culture>: asking about the user's preferred cuisine type or cooking style
      <exercise>: asking about the user's exercise habit, whether the user often exercise or not
      
      I am managing the flow of a conversation including various topics related to user's eating habits. The Definition of topics are listed above. 
      In [conversation log] below, the topics are delivered to the user by asking corresponding questions relevant to the Definition of topics above. For instance, the chabot may deliver <culture> topic by asking 'By the way, do you have a preferred cuisine type or cooking style?'
      According to the [conversation log] below, I judge if questions corresponding to the topics in [asked topics] were all successfully asked and user was clear about them. If a certain topic in [asked topics] is overlooked, forgot to deliver, or the user is not clear about its meaning, output the topic.
      If all topics in [asked topics] are successfully delivered, I will output 'OK'.
      
      [conversation log]->
      {conv}
      '''.format(conv=conv)
    
    client = OpenAI(api_key = "your_api_key")

    interface = "\My output:"
    prompt = controllerprompt + interface
    
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0.3,
      max_tokens=15,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )  

    res = response.choices[0].message.content
    res = res.replace("<", "").replace(">", "").replace("'", "")
    
    if res in origintask:
      if len(pretasks) >= 2 and pretasks[-2] != res:
        if tasklst == 'finished':
          print('module output result: ', res)
          dbops.upcurrenttask(uid, res)
          dbops.upprevtasklst(uid, res)
          return res
        else:
          if res in avaitask:
            print('select an available task')
            print('module output result: ', res)
            dbops.upcurrenttask(uid, res)
            dbops.upprevtasklst(uid, res)
            return res
          else:
            print('select an unavailable task')
            print('module output result: ', res)
            rantask = random.choice(tasklst)
            dbops.upcurrenttask(uid, rantask)
            dbops.upprevtasklst(uid, rantask)
            return rantask
      elif len(pretasks) >= 2 and pretasks[-2] == res:
        if tasklst == 'finished':
          return 'OK'
        else:
          randomtopic = random.choice(tasklst)
          dbops.upcurrenttask(uid, randomtopic)
          dbops.upprevtasklst(uid, randomtopic)
          return randomtopic
      else:
        if res in avaitask:
          print('select an available task')
          print('module output result: ', res)
          dbops.upcurrenttask(uid, res)
          dbops.upprevtasklst(uid, res)
          return res
        else:
          print('select an unavailable task')
          print('module output result: ', res)
          rantask = random.choice(tasklst)
          dbops.upcurrenttask(uid, rantask)
          dbops.upprevtasklst(uid, rantask)
          return rantask
    else:
      print('mistake, output: ', res)
      if tasklst == 'finished':
        return 'OK'
      else:
        randomtopic = random.choice(tasklst)
        dbops.upcurrenttask(uid, randomtopic)
        dbops.upprevtasklst(uid, randomtopic)
        return randomtopic

#intentdetection('55c37e1cfdf99b3f595dc7ffemailprolificcom')