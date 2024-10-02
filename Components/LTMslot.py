from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

import json

#The slot filler may be needed to change. Conversation input is a little bit weird.
#uid = 'asdkhasd'

def LTMslot_interface(uid):
    client = OpenAI(api_key = "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")
    
    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ','')
    user = lst[1]
    av = str(Avery)
    us = str(user)
    
    slot_prompt = '''
    Extract and conclude the information about user's *resource constraints*, *religion*, or *special health condition* in the <conversation>. 
    *resource constraints* covers *budget constraints*, *eating time or dining environment constraints*, or *food accessibility or cooking tools constraints*.
    If the user does not express above information in the <conversation>, your output must be 'none'.
    Examples:
    <conversation>:
    chatbot: By the way; do you like eating out or cooking for yourself?
    user: I like eating out but it costs much so cook at home a lot.
    Your output: the user has a tight budget of food.
    
    <conversation>:
    chatbot: You mentioned reducing acid reflux. Could you share more about that?
    user: I have issues with acid reflux damaging my vocal chords. It would be nice to focus on meals that minimize this.
    Your output: the user has issues with acid reflux and want foods that can minimize this.
    
    <conversation>:
    chatbot: By the way; how's life treating you lately?
    user: I am eating it slowly though. I just eat smaller portions. Also it's been alright I guess. Just tired and low on energy. It's also ramadan so i'm fasting.
    Your output: the user believes in Islam and is currently fasting in the ramadan.
    
    <conversation>:
    chatbot: Good to hear that you are listening to your body signals! Btw, what do you always eat in daily lives?
    user: Beef noodles.
    Your output: none
    
    <conversation>:\n
    '''
  
    
    coversation = 'chatbot: ' + av + '\n' + 'user: ' + us
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
    print('LTMoutput: ', res)
    if res != 'none':
        dbops.updateLTM(uid, res)
  

#Avery = 'OK I understand how you feel man, then what is your eating goal of this meal?'
#User = 'I need to gain weight.'
#res = slot_interface(Avery, User)
#print(res)
