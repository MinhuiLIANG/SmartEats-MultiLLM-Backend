import openai
import sys 
sys.path.append("..") 
import fixedSentences
from Components import slotFiller4pre
from Components import imageGenerator
from Components import paraphraser
from Components import slotFiller4FB
from DAO import dbops
import json

uid = "asdkhasd"
  
def rec_interface(round):
    if round == 'one':
      slotFiller4pre.profile_editor()
      prefix = fixedSentences.prefixes["rec"]
      aftfix = fixedSentences.prefixes["aftrec1"]
    if round == 'two':
      dbops.upaccfrst(uid,'False')
      slotFiller4FB.profile_editor()
      prefix = fixedSentences.prefixes["recfb"]
      aftfix = fixedSentences.prefixes["aftrec2"]

    cal = dbops.getcal(uid)
    loc = dbops.getloc(uid)
    con = dbops.getcon(uid)
    goal = dbops.getgoal(uid)
    emo = dbops.getemo(uid)
    hun = dbops.gethunger(uid)
    limit = dbops.getlimit(uid)
    prefer = dbops.getprefer(uid)
    fb = dbops.getlastusersent(uid).replace("user:","")
    
    chitchatPrompt = '''
    *Your information:
    [calorie limitation] -> {cal}
    [location] -> {loc}
    [contraindication] -> {con}
    [emotion] -> {emo}
    [hunger level] -> {hun}
    [time limitation] -> {limit}
    [eating goal] -> {goal}
    [preference] -> {prefer}
    [feedback] -> {fb}
    
    *Requirements:
    1: The calorie of food I recommend should not be above [calorie limitation] of *Your information.
    2: The food I recommend should be in keeping with the local flavor, and can be easily found locally according to [location] of *Your information.
    3: If your [emotion] is <positive>, I will recommend more delicious and pleasant food; if user's emotion is <negative>, I will recommend comfort food, with warm, soft, sweet taste, and reward you with appropriate junk food like chips and ice cream.
    4: If your [hunger level] is <prominent>, I will recommend more carb-heavy, satiating foods; if user's [hunger level] is <marginal>, I will recommend more fruits and vegetables, light and refreshing flavored foods.
    5: If your [time limitation] is <marginal>, I will recommend common, easy to get food, such as fast food.
    6: I will NEVER recommend food in [contraindication], because it is rude to recommend what you dislike.
    7: I will recommend food which echos to the [eating goal].
    8: I will recommend food which echos to the [preference] of you.
    9: I will consider the [feedback] before making recommendation if it is not 'none'.
    
    I am a professional nutritionist, I will recommend two healthy, balanced and personalized foods for you according to the *Your information and *Requirements above. I would prioritize [location], [contraindication], and [preference] when making recommendations. Also, I will recommend different kinds of food in the two recommendations.
    Each recommendation is followed by the reason why I recommend this to you. I will prioritize [emotion], [hunger level], [time limitation] and [eating goal] in explaining my reasoning.
    The recommend and reason is separated by '[cat]'; the two recommendations are separated by '[sep]'.
    So my recommendation should be like: 1, recommendation [cat] reason [sep] 2, recommendation [cat] reason.
    
    '''.format(cal=cal,loc=loc,emo=emo,hun=hun,limit=limit,con=con,goal=goal,prefer=prefer,fb=fb)  
    
    openai.api_key = "your_api_key"
    interface_answer = '\nMy recmendation: '
    prompt = chitchatPrompt + interface_answer
    response = openai.Completion.create(
      model="gpt-3.5-turbo-instruct",
      prompt=prompt,
      temperature=0.5,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
    )
    res = response.choices[0].text.strip('\n').strip(' ')
    lst = res.split('[sep]')
    if len(lst) > 1:
        rec1 = lst[0].replace('\n','').replace('[cat]','')
        rec2 = lst[1].replace('\n','').replace('[cat]','')
        rec_1_paraed = paraphraser.para_interface(rec1)
        rec_2_paraed = paraphraser.para_interface(rec2)
        img1, food1 = imageGenerator.imageGenerate(rec1)
        img2, food2 = imageGenerator.imageGenerate(rec2)
        meta = food1 + ", " + food2
        dbops.upcon(uid,meta)
        metachat = prefix + "[SEP]" + rec_1_paraed + "[SEP]" + rec_2_paraed + "[SEP]" + aftfix
        dbops.upconversation_b(uid,metachat)
        return {"prefix":prefix,"rec1":rec_1_paraed,"rec2":rec_2_paraed,"img1":img1,"img2":img2,"afterfix":aftfix}
    else:
        rec = lst[0].replace('\n','').replace('[cat]','').replace('[sep]','')
        rec_paraed = paraphraser.para_interface(rec)
        img, food = imageGenerator.imageGenerate(rec)
        dbops.upcon(uid,food)
        metachat = prefix + "[SEP]" + rec_paraed + "[SEP]" + aftfix
        dbops.upconversation_b(uid,metachat)
        return {"prefix":prefix,"rec1":rec_paraed,"rec2":'none',"img1":img,"img2":'none',"afterfix":aftfix}

