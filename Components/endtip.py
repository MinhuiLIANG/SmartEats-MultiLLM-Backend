from openai import OpenAI
import sys

sys.path.append("..")
from DAO import dbops


# uid = "asdkhasd"
def getips(uid):
    loc = dbops.getloc(uid)
    con = dbops.getcon(uid)
    cal = dbops.getcal(uid)
    place = dbops.getenv(uid)
    pre = dbops.getprefer(uid)
    preferfood = dbops.getpreferencefood(uid)
    health = dbops.getconcern(uid)
    his = dbops.gethistory(uid)
    eh = dbops.geteh(uid)
    emo = dbops.getemo(uid)
    limit = dbops.getlimit(uid)
    goal = dbops.getgoal(uid)

    confoodlst = con.split(", , ")
    confood = confoodlst[0]

    prompt = '''
    *Profile:
    [current location] -> {location}
    [food restriction] -> {foodrestriction}
    [calorie limit] -> {calorie}
    [eating environment] -> {diningenvironment}
    [preference] -> {dietarypreference} and {specificpreferedfood}
    [health concern] -> {healthconcern}
    [diet history] -> {diethistory}
    [eating habit] -> {eatinghabit}
    [recent emotion] -> {emotion}
    [time for eating] -> {timelimitation}
    [eating goal] -> {eatinggoal}
   
    I am a nutritionist. The above information points are the user's *Profile about health condition and diet information. I will provide *ONE SHORT* tip about healthy eating that is beneficial to the user's [health concern] and [eating goal]. I will carefully consider all the information in the user's *Profile and select only two to three pieces of information that are deemed to be important and beneficial to compose a dietary tip. This tip should NOT cover more than three pieces of information. I will focus on the information in the user's *Profile which is important. My tip is concise and in plain language. 
    After providing the tip, I will extract two or three keywords from the tip and start a new line to show the keywords. The keywords need to be specific and professional, and start with 'Here are the dietary keywords for you: ' (e.g., Here are the dietary keywords for you: moderate sodium, a mix of carbs, regular exercise).
    My tip and keywords:
    '''.format(
        location=loc, foodrestriction=confood, calorie=cal, dietarypreference=pre, specificpreferedfood=preferfood, healthconcern=health, diningenvironment=place, diethistory=his, eatinghabit=eh, emotion=emo, timelimitation=limit, eatinggoal=goal)

    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=196,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    res = response.choices[0].message.content
    print('tip: ', res)
    return res