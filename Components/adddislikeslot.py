from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

import json

#The slot filler may be needed to change. Conversation input is a little bit weird.
#uid = 'asdkhasd'

def disslot_interface(uid):
    client = OpenAI(api_key = "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")
    
    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ','')
    user = lst[1]
    av = str(Avery)
    us = str(user)
    
    slot_prompt = '''
    Extract the food name or type in the <conversation> if User mentioned he/she *dislike*, *can NOT eat*, or *do NOT want* the food. If there is no food name or the User does not express food preference in the <conversation>, your output must be 'none'.
    Examples:
    <conversation>:
    Avery: OK I am glad that you have plenty of leisure time, I think Korean hot pot can be a good choice for you to enjoy your meal! What kind of food do you usually eat when you are not very busy?
    User: I want some food similar to the Korean hot pot, I don't like grilled chicken breast.
    Your output: grilled chicken breast
    
    <conversation>:
    Avery: That's awesome, Love hearing that you're feeling good. Been experimenting with any new eats or just loving on the usual faves lately?
    User: I don't want fat meats.
    Your output: fat meats
    
    <conversation>:
    Avery: Eating regularly is a good choice to manage your health condition, so, how do you feel about that?
    User: I feel good.
    Your output: none
    
    <conversation>:
    Avery: Good to hear that you are listening to your body signals! Btw, what do you always eat in daily lives?
    User: Beef noodles.
    Your output: none
    
    <conversation>:\n
    '''
  
    
    coversation = 'Avery: ' + av + '\n' + 'User: ' + us
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
    if res != 'none':
        dbops.upcon(uid, res)
  

#Avery = 'OK I understand how you feel man, then what is your eating goal of this meal?'
#User = 'I need to gain weight.'
#res = slot_interface(Avery, User)
#print(res)
