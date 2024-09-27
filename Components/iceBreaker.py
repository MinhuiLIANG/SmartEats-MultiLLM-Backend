from openai import OpenAI
import sys

sys.path.append("..")
from Components import paraphraser
from DAO import dbops


# get it from frontend
# uid = "asdkhasd"
def iceBreak_interface(uid):
    persona = dbops.getpersona(uid)
    location = dbops.getloc(uid)
    style = dbops.getstyle(uid)
    cha = dbops.getchara(uid)
    iceBreakPrompt = '''
    *Personality: {personality}
    *Conversational Style: {style}
    *Additional Characteristics: {Characteristics}
   
    I am SmartEats, a nutrition expert here to provide personalized dietary recommendations for people. My *Personality, *Conversational Style, and *Additional Characteristics are listed above.
    I start a conversation by greeting the user with a brief self-introduction. Note that in the self-introduction I will NOT ask any questions, such as 'How can I assist you today?', 'Ready to start?'. If *Personality is 'extroverted' and *Conversational Style is 'casually', I may send some emojis.
    I always use plain and concise language to communicate with people and will not repeat myself. Moreover, I keep my words short.
    '''.format(personality=persona,style=style,Characteristics=cha)

    client = OpenAI(api_key="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")

    interface = "\nMy words: "
    prompt = iceBreakPrompt + interface

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=196,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    res = response.choices[
              0].message.content + "\n\nIn this conversation, we'll delve into your dietary preferences, lifestyle, and health goals. Based on the information, I'll try to search for some food that meet your needs and see if you would like to try them out in the upcoming week. Ready to start?"
    return res