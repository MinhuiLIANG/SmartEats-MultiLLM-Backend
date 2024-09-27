from openai import OpenAI
import sys

sys.path.append("..")
from DAO import dbops


# uid = "asdkhasd"
def prerect_interface(uid):
    loc = dbops.getloc(uid)
    con = dbops.getcon(uid)
    cal = dbops.getcal(uid)
    place = dbops.getenv(uid)
    pre = dbops.getprefer(uid)
    preferfood = dbops.getpreferencefood(uid)
    health = dbops.getconcern(uid)
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
        [preference]-><{dietarypreference}>
        [health concern]-><{healthconcern}>
        
        *Task -> List five *non-traditional* cuisines that are very *popular*, loved, and widely eaten by people in [location] according to the information above. Do not recommend anything peculiar.
        *Rules ->
        1. Each dish you list must be a combination of two foods: one main food and one side food, they must be nutritionally balanced and varied, including vitamins, carbs, and protein.
        2. Each dish needs to be below [calorie restriction].
        3. You must consider [dietary restriction] in your listed dishes if the it is not 'none'.
        4. People provide [feedback] regarding [first food] and [second food], which were recommended by you previously. Make another recommendation according to this information. If the people explicitly mention in the *feedback* the specific, healthy enough food they desire, I will list that dish.
        5. Be careful about people's [health concern] if it is not 'none', the dishes should be safe and beneficial to it. This requirement has the highest priority.
        6. For each dish, the main food is the one that fits people's [preference] and [health concern] if they are not 'none'. You should first determine the main food and it should be specific. The side food is other foods to provide a balanced and rich diet. The side food can be less specific, such as 'rice', 'vegetable', and  'fruits'. Note that the combination of main food and side food must be nutritionally balanced, including vitamins, carbs, and protein.
        7. The dishes can be a little bit surprising and trendy.
        8. Just list the dishes and do not explain the reason.
        For example, in the food 'Grilled salmon with quinoa and steamed broccoli', if people's [health concern] is about <blood pressure>, then the main food is 'steamed broccoli' because its fiber and minerals are good for blood pressure. The side food is 'Grilled salmon with quinoa', no need to be this specific, you should summarize it. So the food you list should be 'seafood with quinoa and steamed broccoli'.
        *Example->
        cheesecake with mango pudding
        grilled steak and fruit salad with bread
        List the five dishes here following the *Rules and *Example above. Use your knowledge to make the five dishes very *attractive*, *diverse* and *different from each other*. You must make sure people with different [location], [dietary restrictions], [preference], and [health concern] will receive different dishes. Personalization Matters!
        '''.format(location=loc, dietaryrestriction=con, calorie=cal, dietarypreference=pre,
            healthconcern=health, firstrecommendedfoodfromlastround=f1,
            secondrecommendfoodfromlastround=f2, feedback=fb)
    else:
        prompt = '''
        [location]-><{location}>
        [calorie restriction]-><{calorie}>
        [dietary restriction]-><{dietaryrestriction}>
        [preference]-><{dietarypreference}>
        [health concern]-><{healthconcern}>
        
        *Task -> List five *non-traditional* cuisines that are very *popular*, loved, and widely eaten by people in [location] according to the information above. Do not recommend anything peculiar.
        *Rules ->
        1. Each dish you list must be a combination of two foods: one main food and one side food, they must be nutritionally balanced and varied, including vitamins, carbs, and protein.
        2. Each dish needs to be below [calorie restriction].
        3. You must consider [dietary restriction] in your listed dishes if the it is not 'none'.
        4. Be careful about people's [health concern] if it is not 'none', the dishes should be safe and beneficial to it. This requirement has the highest priority.
        5. For each dish, the main food is the one that fits people's [preference] and [health concern] if they are not 'none'. You should first determine the main food and it should be specific. The side food is other foods to provide a balanced and rich diet. The side food can be less specific, such as 'rice', 'vegetable', and  'fruits'. Note that the combination of main food and side food must be nutritionally balanced, including vitamins, carbs, and protein.
        6. The dishes can be a little bit surprising and trendy.
        7. Just list the dishes and do not explain the reason.
        For example, in the food 'Grilled salmon with quinoa and steamed broccoli', if people's [health concern] is about <blood pressure>, then the main food is 'steamed broccoli' because its fiber and minerals are good for blood pressure. The side food is 'Grilled salmon with quinoa', no need to be this specific, you should summarize it. So the food you list should be 'seafood with quinoa and steamed broccoli'.
        *Example->
        cheesecake with mango pudding
        grilled steak and fruit salad with bread
        List the five dishes here following the *Rules and *Example above. Use your knowledge to make the five dishes very *attractive*, *diverse* and *different from each other*. You must make sure people with different [location], [dietary restrictions], [preference], and [health concern] will receive different dishes. Personalization Matters!
        '''.format(location=loc, dietaryrestriction=con, calorie=cal, dietarypreference=pre,
            healthconcern=health)

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