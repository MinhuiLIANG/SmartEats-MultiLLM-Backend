from openai import OpenAI
import sys

sys.path.append("..")
from DAO import dbops

import json


# The slot filler may be needed to change. Conversation input is a little bit weird.
# uid = 'asdkhasd'

def preslot_interface(uid):
    client = OpenAI(api_key="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")

    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ', '')
    user = lst[1]
    av = str(Avery)
    us = str(user)

    slot_prompt = '''
    Extract the food name or type in the <conversation> if User mentioned he/she *like*, *prefer* or *want* the food. If there is no food name or the User does NOT express food preference although there are foods names (e.g., in 'I often have some grilled chicken breast', the User did not mention he/she likes grilled chicken breast) in the <conversation>, your output must be 'none'.
    Examples:
    <conversation>:
    Avery: OK I am glad that you have plenty of leisure time, I think Korean hot pot can be a good choice for you to enjoy your meal! What kind of food do you usually eat when you are not very busy?
    User: I want some food similar to the Korean hot pot.
    Your output: Korean hot pot

    <conversation>:
    Avery: That's awesome, Love hearing that you're feeling good. Been experimenting with any new eats or just loving on the usual faves lately?
    User: i like beef, prawn, and green vegetables
    Your output: beef, prawn, and green vegetables

    <conversation>:
    Avery: Eating regularly is a good choice to manage your health condition, so, how do you feel about that?
    User: I feel good.
    Your output: none

    <conversation>:
    Avery: Good to hear that you are listening to your body signals! Btw, what do you always eat in daily lives?
    User: I usually have some beef noodles and garlic.
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
    fd = dbops.getpreferencefood(uid)
    if fd == 'none':
        dbops.uppreferencefood(uid, res)

# Avery = 'OK I understand how you feel man, then what is your eating goal of this meal?'
# User = 'I need to gain weight.'
# res = slot_interface(Avery, User)
# print(res)
