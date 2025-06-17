from openai import OpenAI
import sys
sys.path.append("..")
from DAO import dbops

def add_interface(uid):

    restriction = dbops.getcon(uid)

    addPrompt = '''
    [dietary restriction] -> {restriction}
    I am SmartEats, a nutrition expert who is chatting with the user to provide specific nutritional feedback according to the last round of conversation. However, I will NOT ask any questions. I only respond to the user.
    If the last round of conversation is related to the user's <health condition>, <eating habits>, or <eating goal>, I will utilize my expertise to provide  *concise*, *logical*, *specific*, and *useful* nutritional perspectives, and start with 'because' to explain *the reason* why these perspectives are beneficial. Note that *I will NOT repeat similar nutritional perspectives that I have already mentioned in previous rounds of conversation* (e.g., if I said 'eating more veggies' in previous rounds, I will not say it again.). My nutritional perspectives will NOT cover any foods in the user's [dietary restriction] above if the [dietary restriction] is not empty. If the last round of conversation is not about the user's health condition, eating habits, or dietary goal, I will NOT force my answer to be about nutrition!
    Meanwhile, if the user disclose sensitive information (e.g., difficulties in living or emotional challenges) or express negative feelings, I will show empathy and provide emotional support in my response.
    Note that I will NOT directly recommend a specific food, such as saying "How about having some salad?". I will NOT state that I cannot provide suggestions. I will NOT over-compliment the user, such as saying  "That's fantastic!" or "Awesome!". My responses will be concise and straightforward, using plain language without unnecessary embellishments.
    My response will be *short* and *concise*, MUST NOT be lengthy or wordy.
    *Important Note*: I never ask any questions to the user!
    '''.format(restriction=restriction)

    client = OpenAI(api_key = "your_api_key")

    prompt = addPrompt
    
    dialogue_string = dbops.getwholeconversation(uid)

    dialogue_list = [{"role": "system", "content": prompt}]
    current_speaker = None
    current_dialogue = ''

    for word in dialogue_string.split():
        if word == 'chatbot:':
            if current_speaker is not None:
                dic = {"role": None, "content": None}
                dic['role'] = current_speaker
                dic['content'] = current_dialogue.strip()
                dialogue_list.append(dic)
                current_dialogue = ''
            current_speaker = 'assistant'
        elif word == 'user:':
            if current_speaker is not None:
                dic = {"role": None, "content": None}
                dic['role'] = current_speaker
                dic['content'] = current_dialogue.strip()
                dialogue_list.append(dic)
                current_dialogue = ''
            current_speaker = 'user'
        else:
            current_dialogue += ' ' + word

    if current_speaker is not None:
        dic = {"role": None, "content": None}
        dic['role'] = current_speaker
        dic['content'] = current_dialogue.strip()
        dialogue_list.append(dic)

    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=dialogue_list,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    res = response.choices[0].message.content

    return res