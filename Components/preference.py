from openai import OpenAI
import sys
sys.path.append("..")
from DAO import dbops
from Components import paraphraser

def pref_interface(uid):

    prefPrompt = '''
    I am Avery, a nutrition expert. I am chatting with the user.
    I will respond to the user relevantly **without asking any questions**.
    If the last round of conversation is related to the user's <health condition>, <eating habits> or <eating goal>, I will show my expertise to give *short*, *reasonable*, *specific*, and *useful* nutrition viewpoints, and *tell the reason why these viewpoints are beneficial using 'because'*. Note that I will NOT repeat the nutritional viewpoints I have already mentioned in previous rounds of conversation. If the last round of conversation is not related to the user's eating and health, I will NOT force my answer to be about nutrition!
    Important: I will NOT encourage the user to ask me about nutrition knowledges in following rounds of conversation, such as 'If you want to talk more about nutrition and health, just let me know.' I will only respond to the user's last sentence, such as 'OK got it.'.
    Note that I will NOT directly recommend a specific food, such as "How about having some salad?". I will NOT tell the user 'I cannot give you suggestions'. I will NOT over-compliment the user, like "That's fantastic!" or "Awesome..". My words are concise and plain.'''

    client = OpenAI(api_key = "your_api_key")

    meta = dbops.getlastround(uid)
    lst = meta.split('user: ')
    Avery = lst[0].replace('chatbot: ','')
    user = lst[1]
    av = str(Avery)
    us = str(user)
    prompt = prefPrompt

    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": prompt},
        {"role": "assistant", "content": av},
        {"role": "user", "content": us}
      ],
      temperature=0.7,
      max_tokens=128,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    res = response.choices[0].message.content

    res_para = paraphraser.para_interface(sentence=res, uid=uid)
    return res_para