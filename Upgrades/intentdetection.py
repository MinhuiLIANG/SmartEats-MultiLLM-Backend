from openai import OpenAI
import random
import sys 
sys.path.append("..") 
from DAO import dbops

#uid = 'asdkhasd'
def intentdetection(uid):
    origintask = ['emotion', 'env', 'goal', 'his', 'hunger level', 'time limitation']
    tasklst = dbops.gettasklst(uid)
    print('tasklist: ', tasklst)

    conv = dbops.getwholeconversation(uid)
    
    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ','')
    user = lst[1]
    av = str(Avery)
    us = str(user)
    coversation = 'chatbot: ' + av + '\n' + 'user: ' + us
    lasttask = dbops.getlasttask(uid)
    print('last topic: ', lasttask)
    controllerprompt = ''
    if tasklst != 'finished':
      controllerprompt = '''
      Definition of topics:
      emotion: asking about the user's recent emotion status
      env: asking about the user's daily dining environment, eating outside or cooking at home
      goal: asking about the user's dietary goal or requiring user to further elaborate health conditions
      his: asking about the user's general daily food patterns
      hunger level: asking about the user's eating habits, whether the user eat regularly or just eat when hungry.
      time limitation: asking about how much time the user can spend for a meal.
      
      [rest topics]-><{}>
      [last topic]-><{lasttask}>
      [conversation log]->{coversation}
      
      I am a chatbot managing the flow of a conversation including various topics related to user's eating habits. The Definition of topics are listed at the beginning. [last topic] represents the topic I just delivered, [rest topics] represents the topics I am going to ask, [conversation log] records how I delivered the last topic and the user's reaction to it.
      I manage the conversation flow by select a topic from [rest topics] and [last topic]. I MUST NOT select any topic not belonging to [rest topics] or [last topic]!
      According to the [conversation log], I judge if the [last topic] were successfully asked and user was clear about it. If the I forgot to ask or user ask for further elaboration, I output the value of [last topic] (in <>).
      If the [last topic] was successfully delivered, then I output a certain topic from [rest topics] which can make the conversation flow smoothly, natural and coherent. I will not deliver [last topic] again.
      '''.format(", ".join(tasklst), lasttask=lasttask, coversation=coversation)
    else:
      controllerprompt = '''
      [asked topics]-><'emotion', 'env', 'goal', 'his', 'hunger level', 'time limitation'>
      
      Definition of topics:
      emotion: asking about the user's recent emotion status
      env: asking about the user's daily dining environment, eating outside or cooking at home
      goal: asking about the user's dietary goal or requiring user to further elaborate health conditions
      his: asking about the user's general daily food patterns
      hunger level: asking about the user's eating habits, whether the user eat regularly or just eat when hungry.
      time limitation: asking about how much time the user can spend for a meal.
      
      I am a chatbot managing the flow of a conversation including various topics related to user's eating habits. [asked topics] represents the topics I have delivered.
      According to the [conversation log] below, I judge if topics in [asked topics] were successfully asked and user was clear about them. If I forgot to ask or user was not clear about a certain topic in [asked topics], output the topic user was not clear.
      If all topics in [asked topics] is successfully delivered, I will output 'OK'.
      
      [conversation log]->{conv}
      '''.format(conv=conv)
    
    client = OpenAI(api_key = "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")

    interface = "\My output:"
    prompt = controllerprompt + interface
    
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0,
      max_tokens=15,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )  

    res = response.choices[0].message.content
    res = res.replace("<", "").replace(">", "").replace("'", "")
    
    if res in origintask:
      print('module output result: ', res)
      return res
    else:
      print('mistake, output: ', res)
      if tasklst == 'finished':
        return 'OK'
      else:
        randomtopic = random.choice(tasklst)
        return randomtopic

#intentdetection('55c37e1cfdf99b3f595dc7ffemailprolificcom')