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
    topic 1: <emotion> -> values 1: [<positive>, <neutral>, <negative>]
    topic 2: <eating habit> -> values 2: [<regular>, <casual>]
    topic 3: <time limitation> -> value 3: [<limited>, <neutral>, <sufficient>]
    topic 4: <goal> -> value 4: [User's sentence]
    topic 5: <environment> -> value 5: [<outside>, <home>]
    topic 6: <eating history> -> value 6: [Food type in User's sentence]

    The above pairs show the map of topics and values, each topic (such as <emotion>) relates to several values (such as <positive>, <neutral>, <negative>).
    There will be a single round conversation, in which the assistant asks a question related to one of the topics shown above.
    Then the User will respond. Please output the one value in values related to the topic the assistant asks according to the content of the User's response.

    Here are two examples:
    assistant: I understand how you feel. Hunger can be quite distracting. So, how much time do you have to eat right now?
    User: I have limited time for the meal.
    
    assistant: Hi it's great to see you too! How can I assist you today? Let's talk about your eating goals or any health plans you may have.
    User: I think I want to lose weight.

    First, you need to judge what is the topic according to the assistant's words. In the first example, 'how much time do you have to eat right now?' indicates the topic is <time limitation>;
    in the second example, 'Let's talk about your eating goals or any health plans you may have.' means that the assistant is asking about User's goal, so the topic is <goal>.
    
    Second, you need to judge what value is related to the topic you just find according to the User's words. If the value is abstract, like [Food type in User's sentence], you should extract the food information in the user's sentence as the value. In the first example, 'limited time for the meal' means the <time limitation> is <limited>;
    in the second example, the value of <goal> is the user's sentence, so the value is <I think I want to lose weight.>, just set the value to the user's original sentence.
    
    So your output of the first example is: <time limitation>:<limited>; for the second example, it is <goal>:<I think I want to lose weight.>
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
  print("********", res)
  lst = res.split(':')
  topic_list = ['emotion', 'eating habit', 'time limitation', 'goal', 'environment', 'eating history']
  value_list = ['positive', 'neutral', 'negative', 'limited', 'sufficient', 'regular', 'casual', 'outside', 'home']
  if len(lst)>1:
    topic = lst[0].replace('<','').replace('>','')
    value = lst[1].replace('<','').replace('>','')
    if topic in topic_list and value in value_list:
      if topic == 'emotion':
        dbops.upemo(uid, value)
      if topic == 'eating habit':
        dbops.upeh(uid, value)
      if topic == 'time limitation':
        dbops.uplimit(uid, value)
      if topic == 'environment':
        dbops.upenv(uid, value)
    elif topic == 'goal':
      dbops.upgoal(uid, value)
    elif topic == 'eating history':
      dbops.uphistory(uid, value)
  

#Avery = 'OK I understand how you feel man, then what is your eating goal of this meal?'
#User = 'I need to gain weight.'
#res = slot_interface(Avery, User)
#print(res)
