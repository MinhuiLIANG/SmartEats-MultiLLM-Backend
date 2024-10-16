from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

import json

#The slot filler may be needed to change. Conversation input is a little bit weird.
#uid = 'asdkhasd'

def slot_interface(uid):
    client = OpenAI(api_key = "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")
    
    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ','')
    user = lst[1]
    av = str(Avery)
    us = str(user)
    
    slot_prompt = '''
    topic 1: <biological sex> -> values 1: [<female>, <intersex>, <male>]
    topic 2: <age> -> values 2: [the user's age number]
    topic 3: <height> -> value 3: [the number of user's height (cm)]
    topic 4: <weight> -> value 4: [the number of user's weight (kg)]
    topic 5: <region> -> value 5: [user's region]
    topic 6: <dietary restriction> -> value 6: [user's dietary restriction]

    The above pairs show the map of topics and values, each topic (such as <biological sex>) relates to several values (such as <female>, <intersex>, <male>) or the value need to be extracted from the user's response (such as topic <age> and [the user's age number]).
    There will be a single round conversation, in which the assistant asks a question related to one of the topics shown above.
    Then the User will respond. Please output the value in values related to the topic the assistant asks according to the content of the User's response.

    Here are two examples:
    assistant: OK I see. So, could you please tell me your age?
    User: Sure, I am 20 years old.
    
    assistant: Let's go. May I ask how tall are you?
    User: I am 181 cm tall.
    
    First, you need to judge what is the topic according to the assistant's words. In the first example, 'could you please tell me your age?' indicates the topic is <age>;
    in the second example, 'May I ask how tall are you?' means that the assistant is asking about User's height, so the topic is <height>.
    
    Second, you need to judge what value is related to the topic you just find according to the User's message. If the value is abstract, like [the number of user's height (cm)], you should extract the height number in the user's message as the value. In the first example, 'Sure, I am 20 years old.' means the <age> is <20>;
    in the second example, the value of <height> is the number of user's height (cm) in the response, so the value is <181>, just extract the number without measurement unit (cm) in the user's response.
    So your output of the first example is: <age>:<20>; for the second example, it is <height>:<181>.
    
    Now try this conversation:\n
    '''
  
    
    coversation = 'assistant: ' + av + '\n' + 'User: ' + us
    interface = '\nYour output: '
    prompt = slot_prompt + coversation + interface
    
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0,
      max_tokens=96,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )
    res = response.choices[0].message.content
    return res
  
def profile_editor(uid):
  res = slot_interface(uid)
  print("********aka", res)
  lst = res.split(':')
  topic_list = ['biological sex', 'age', 'height', 'weight', 'region', 'dietary restriction']
  if len(lst)>1:
    topic = lst[0].replace('<','').replace('>','')
    value = lst[1].replace('<','').replace('>','')
    if topic in topic_list:
      if topic == 'biological sex':
        dbops.upgender(uid, value)
      if topic == 'age':
          try:
            number = float(value)
            if number >= 18 and number <= 70:
                dbops.upage(uid, number)
          except ValueError:
            dbops.upage(uid, 33)
      if topic == 'height':
          try:
            number = float(value)
            if number >= 100 and number <= 250:
                dbops.upheight(uid, number)
          except ValueError:
            dbops.upheight(uid, 170)
      if topic == 'weight':
          try:
            number = float(value)
            if number >= 30 and number <= 150:
                dbops.upweight(uid, number)
          except ValueError:
            dbops.upweight(uid, 65)
      if topic == 'region':
        dbops.uploc(uid, value)
      if topic == 'dietary restriction':
        dbops.upcon(uid, value)
  

#Avery = 'OK I understand how you feel man, then what is your eating goal of this meal?'
#User = 'I need to gain weight.'
#res = slot_interface(Avery, User)
#print(res)
