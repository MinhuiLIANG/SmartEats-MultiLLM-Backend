from openai import OpenAI
import sys

sys.path.append("..")
from DAO import dbops


# uid = "asdkhasd"
def prereco_interface(uid):
    loc = dbops.getloc(uid)
    con = dbops.getcon(uid)
    cal = dbops.getcal(uid)
    place = dbops.getenv(uid)
    pre = dbops.getprefer(uid)
    preferfood = dbops.getpreferencefood(uid)
    preferflavor = dbops.getflavorpreference(uid)
    goal = dbops.getgoal(uid)
    his = dbops.gethistory(uid)
    lastroundfoods = dbops.getallfoods(uid)
    
    budget = dbops.getbudget(uid)
    culture = dbops.getculture(uid)
    social = dbops.getsocial(uid)
    
    if con == '':
        con = 'none'
    
    prompt = ""
    if lastroundfoods != "":
        foodlst = lastroundfoods.split('[FSEP]')
        f1 = foodlst[0]
        f2 = foodlst[1]
        fb = dbops.getlastusersent(uid).replace("user:", "")

        prompt = '''
        [location]-><{location}>
        [calorie restriction]-><{calorie}>
        [dietary restriction]-><{dietaryrestriction}>
        [first food]-><{firstrecommendedfoodfromlastround}>
        [second food]-><{secondrecommendfoodfromlastround}>
        [feedback]-><{feedback}>
        [diet history]-><{diethistory}>
        [dining environmrnt]-><{diningenvironment}>
        [preference]-><{dietarypreference}>
        [preferred food]-><{specificpreferedfood}>
        [preferred flavor]-><{preferflavor}>
        [dietary goal]-><{goal}>
        [budget]-><{budget}>
        [food culture]-><{culture}>
        [social environment of meals]-><{social}>
        
        *Task -> List five *common*, *widely eaten* and *very local* dishes eaten by people in [location] according to the information above. DO NOT list anything peculiar.  
        *Rules ->
        1. Each dish you list must be a combination of two components: one main food and one side food, they must be *nutritionally balanced* and *varied*, including vitamins, carbs, and protein.
        2. Each dish needs to be below [calorie restriction].
        3. You must consider [dietary restriction] in your listed dishes if the it is not 'no' or 'none'.
        4. You should consider [budget] when listing dishes. The dishes you list must be on budget.
        5. People provide [feedback] regarding [first food] and [second food], which were previously recommended by you. Make another recommendation according to this information. If the people explicitly mention specific, healthy enough foods they desire in the *feedback*, I will list dishes containing the foods.
        6. You should consider [food culture] when listing dishes.
        7. The dishes can be similar to people's [diet history]. Moreover, if [social environment of meals] is 'group', you should list the dishes better fit for [diet history].
        8. If the [dining environment] is 'outside', the dishes should be dishes commonly found in restaurants; If the [dining environment] is 'home', the dishes should be easy for cooking at home and the ingredients should be easy to be found in [location].
        9. People's [preference], [preferred food] and [preferred flavor] must be covered with high priority if it is not 'none' or 'no'. If the user explicitly mention specific, healthy enough foods he/she desire, I will try to cover the foods in the listed dishes.
        10. Just list the dishes and do not explain the reason.
        11. For each dish, the main food fits people's [preference], [preferred food], [preferred flavor] and [dietary goal]. You should first determine the main food which must be *specific*. The side food is to balance and enrich the dish, which should be less specific and described in general terms, such as 'seafood', 'vegetable', 'and bread'. Note that the combination of the main food and the side food must be *nutritionally balanced*, including vitamins, carbs, and protein.
        For example, in the food 'Baked salmon with sweet potato mash and avocado salsa' and the user's [dietary goal] is about <cardiovascular function>, then the main food is 'Baked salmon' because the nutrition within salmon is good for heart health; the side food is 'sweet potato mash and avocado salsa', which does not warrant a specific name, you should replace it to a general term. So, the dish you list should be 'Baked salmon with various veggies and sweet potatoes'.
        *Example->
        beef noodles with vegetables
        grilled fish and fruit salad with bread
        List the five dishes here following the *Rules and *Example above for the user. Use your knowledge to make the five dishes very *attractive*, *diverse* and *different from each other*. You must make sure people with different [location], [dietary restrictions], [diet history], [dining environment], [preference], and [dietary goal] will receive different dishes. Personalization Matters!
        '''.format(
                location=loc, dietaryrestriction=con, calorie=cal, dietarypreference=pre, specificpreferedfood=preferfood,
                preferflavor = preferflavor, goal=goal, diningenvironment=place, diethistory=his, firstrecommendedfoodfromlastround=f1,
                secondrecommendfoodfromlastround=f2, feedback=fb, budget=budget, culture=culture, social=social)
    else:
        prompt = '''
        [location]-><{location}>
        [calorie restriction]-><{calorie}>
        [dietary restriction]-><{dietaryrestriction}>
        [diet history]-><{diethistory}>
        [dining environmrnt]-><{diningenvironment}>
        [preference]-><{dietarypreference}>
        [preferred food]-><{specificpreferedfood}>
        [preferred flavor]-><{preferflavor}>
        [dietary goal]-><{goal}>
        [budget]-><{budget}>
        [food culture]-><{culture}>
        [social environment of meals]-><{social}>
        
        *Task -> List five *common*, *widely eaten* and *very local* dishes eaten by people in [location] according to the information above. DO NOT list anything peculiar.  
        *Rules ->
        1. Each dish you list must be a combination of two components: one main food and one side food, they must be *nutritionally balanced* and *varied*, including vitamins, carbs, and protein.
        2. Each dish needs to be below [calorie restriction].
        3. You must consider [dietary restriction] in your listed dishes if the it is not 'no' or 'none'.
        4. You should consider [budget] when listing dishes. The dishes you list must be on budget.
        5. You should consider [food culture] when listing dishes.
        6. The dishes can be similar to people's [diet history]. Moreover, if [social environment of meals] is 'group', you should list the dishes better fit for [diet history].
        7. If the [dining environment] is 'outside', the dishes should be dishes commonly found in restaurants; If the [dining environment] is 'home', the dishes should be easy for cooking at home and the ingredients should be easy to be found in [location].
        8. People's [preference], [preferred food] and [preferred flavor] must be covered with high priority if it is not 'none' or 'no'. If the user explicitly mention specific, healthy enough foods he/she desire, I will try to cover the foods in the listed dishes.
        9. Just list the dishes and do not explain the reason.
        10. For each dish, the main food fits people's [preference], [preferred food], [preferred flavor] and and [dietary goal] if they are not 'none'. You should first determine the main food which must be *specific*. The side food is to balance and enrich the dish, which should be less specific and described in general terms, such as 'seafood', 'vegetable', 'and bread'. Note that the combination of the main food and the side food must be *nutritionally balanced*, including vitamins, carbs, and protein.
        For example, in the food 'Baked salmon with sweet potato mash and avocado salsa' and the user's [dietary goal] is about <cardiovascular function>, then the main food is 'Baked salmon' because the nutrition within salmon is good for heart health; the side food is 'sweet potato mash and avocado salsa', which does not warrant a specific name, you should replace it to a general term. So, the food you list should be 'Baked salmon with various veggies and sweet potatoes'.
        *Example->
        beef noodles with vegetables
        grilled fish and fruit salad with bread
        List the five dishes here following the *Rules and *Example above for the user. Use your knowledge to make the five dishes very *attractive*, *diverse* and *different from each other*. You must make sure people with different [location], [dietary restrictions], [diet history], [dining environment], [preference], and [dietary goal] will receive different dishes. Personalization Matters!
        '''.format(
                location=loc, dietaryrestriction=con, calorie=cal, dietarypreference=pre, specificpreferedfood=preferfood, preferflavor = preferflavor,
                goal=goal, diningenvironment=place, diethistory=his, budget=budget, culture=culture, social=social)

    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=96,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    res = response.choices[0].message.content
    lst = res.split('\n')
    return lst