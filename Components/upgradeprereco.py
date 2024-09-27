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
    health = dbops.getconcern(uid)
    his = dbops.gethistory(uid)
    lastroundfoods = dbops.getallfoods(uid)
    
    if con == '':
        con = 'none'
    
    if health == '':
        health = 'none'
    
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
        [health concern]-><{healthconcern}>
        
        *Task -> List five *common*, *widely eaten* and *very local* dishes eaten by people in [location] according to the information above. Do NOT list anything peculiar.  
        *Rules ->
        1. Each dish you list must be a combination of two components: one main food and one side food, they must be *nutritionally balanced* and *varied*, including vitamins, carbs, and protein.
        2. Each dish needs to be below [calorie restriction].
        3. You must consider [dietary restriction] in your listed dishes if the it is not 'none'.
        4. People provide [feedback] regarding [first food] and [second food], which were recommended by you previously. Make another recommendation according to this information. If the people explicitly mention in the *feedback* the specific, healthy enough food they desire, I will list that dish.
        5. The dishes can be similar to people's [diet history].
        6. If the [dining environment] is 'outside', the dishes should be standard restaurant dishes; If the dining environment is 'home', the dishes should be easy to be made at home and the ingredients should be easy to be found.
        7. People's [preference], such as [preferred food], which must be covered with high priority if it is not 'none'. If the user explicitly mention in the *Preference* the specific, healthy enough food he/she desire, I will list that dish.
        8. Be careful about people's [health concern] if it is not 'none', the dishes should be safe and beneficial to it. This requirement has the highest priority.
        9. Just list the dishes and do not explain the reason.
        10. For each dish, the main food is the one that fits people's [preference] and [health concern] if they are not 'none'. You should first determine the **specific** main food. The side food is other foods to balance and enrich the dish, which should be less specific and described in general terms, such as 'seafood', 'vegetable', 'and bread'. Note that the combination of the main food and the side food must be **nutritionally balanced**, including vitamins, carbs, and protein.
        For example, in the food 'Baked salmon with sweet potato mash and avocado salsa' and the user's [health concern] is about <heart disease>, then the main food is 'Baked salmon' because the nutrition within salmon is good for heart health; the side food is 'sweet potato mash and avocado salsa', which does not warrant a specific name, you should replace it to a general term. So, the food you list should be 'Baked salmon with various veggies and sweet potatoes'.
        *Example->
        beef noodles with vegetables
        grilled fish and fruit salad with bread
        List the five dishes here following the *Rules and *Example above for the user. Use your knowledge to make the five dishes very *attractive*, *diverse* and *different from each other*. You must make sure people with different [location], [dietary restrictions], [diet history], [dining environment], [preference], and [health concern] will receive different dishes. Personalization Matters!
        '''.format(
                location=loc, dietaryrestriction=con, calorie=cal, dietarypreference=pre, specificpreferedfood=preferfood,
                healthconcern=health, diningenvironment=place, diethistory=his, firstrecommendedfoodfromlastround=f1,
                secondrecommendfoodfromlastround=f2, feedback=fb)
    else:
        prompt = '''
        [location]-><{location}>
        [calorie restriction]-><{calorie}>
        [dietary restriction]-><{dietaryrestriction}>
        [diet history]-><{diethistory}>
        [dining environmrnt]-><{diningenvironment}>
        [preference]-><{dietarypreference}>
        [preferred food]-><{specificpreferedfood}>
        [health concern]-><{healthconcern}>
        
        *Task -> List five *common*, *widely eaten* and *very local* dishes eaten by people in [location] according to the information above. Do NOT list anything peculiar.  
        *Rules ->
        1. Each dish you list must be a combination of two components: one main food and one side food, they must be *nutritionally balanced* and *varied*, including vitamins, carbs, and protein.
        2. Each dish needs to be below [calorie restriction].
        3. You must consider [dietary restriction] in your listed dishes if the it is not 'none'.
        4. The dishes can be similar to people's [diet history].
        5. If the [dining environment] is 'outside', the dishes should be standard restaurant dishes; If the dining environment is 'home', the dishes should be easy to be made at home and the ingredients should be easy to be found.
        6. People's [preference], such as [preferred food], which must be covered with high priority if it is not 'none'. If the user explicitly mention in the *Preference* the specific, healthy enough food he/she desire, I will list that dish.
        7. Be careful about people's [health concern] if it is not 'none', the dishes should be safe and beneficial to it. This requirement has the highest priority.
        8. Just list the dishes and do not explain the reason.
        9. For each dish, the main food is the one that fits people's [preference] and [health concern] if they are not 'none'. You should first determine the **specific** main food. The side food is other foods to balance and enrich the dish, which should be less specific and described in general terms, such as 'seafood', 'vegetable', 'and bread'. Note that the combination of the main food and the side food must be **nutritionally balanced**, including vitamins, carbs, and protein.
        For example, in the food 'Baked salmon with sweet potato mash and avocado salsa' and the user's [health concern] is about <heart disease>, then the main food is 'Baked salmon' because the nutrition within salmon is good for heart health; the side food is 'sweet potato mash and avocado salsa', which does not warrant a specific name, you should replace it to a general term. So, the food you list should be 'Baked salmon with various veggies and sweet potatoes'.
        *Example->
        beef noodles with vegetables
        grilled fish and fruit salad with bread
        List the five dishes here following the *Rules and *Example above for the user. Use your knowledge to make the five dishes very *attractive*, *diverse* and *different from each other*. You must make sure people with different [location], [dietary restrictions], [diet history], [dining environment], [preference], and [health concern] will receive different dishes. Personalization Matters!
        '''.format(
                location=loc, dietaryrestriction=con, calorie=cal, dietarypreference=pre, specificpreferedfood=preferfood,
                healthconcern=health, diningenvironment=place, diethistory=his)

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