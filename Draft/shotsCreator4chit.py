from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

uid = 'asdkhasd'

def shots_interface():
    
    task = dbops.gettask(uid)
    client = OpenAI(api_key = "your_api_key")
    
    emotion_context = '''
    *User topics:
    [self introduction]
    [hunger level]
    [time limitation to eat]
    [eating goal]
    
    *Avery topic:
    [emotion]
    
    *Requirements:
    1, User's topic of each conversation is picked in *User topics above one by one.
    2, Avery's question is about [emotion] (how's user feeling) in *Avery topic.
    3, There should be a natural transition between the response to user and the question.
    4, I will make sure User don't ask any questions and Avery don't give suggestions and recommendations.
    5, Avery will only ask 'ONE' question. 
    6, Avery will not call the user by name, like 'Sarah', because it is rude.
    7, Each round only have one sentence from User and one sentence from Avery.
    
    I am an author, my work is imitating and generating a single round of conversation between User and Avery. 
    In one single round of conversation, the user will pick one topic of the four in *User topics above. Then Abvery will provide User considerate and relevant response, and ask a question about *Avery topic above.
    
    [example 1]:
    User: I am not very hungery at this moment.
    Avery: Oh, I guess your last meal was pretty good! Btw, how's your mood today?
    
    [example 2]:
    User: I don't have much time for this meal.
    Avery: Well, you worked hard. So how are you feeling now?

    Now I will write [FOUR] conversations following the instruction and [example] above.
    The four conversations are separated by blank line.
    Add the conversations here:
    '''
    hunger_context = '''
    *User topics:
    [self introduction]
    [emotion]
    [time limitation to eat]
    [eating goal]
    
    *Avery topic:
    [hunger level]
    
    *Requirements:
    1, User's topic of each conversation is picked in *User topics above one by one.
    2, Avery's question is about [hunger level] (if User is hungry) in *Avery topic.
    3, There should be a natural transition between the response to user and the question.
    4, I will make sure User don't ask any questions and Avery don't give suggestions and recommendations.
    5, Avery will only ask 'ONE' question.
    6, Avery will not call the user by name, like 'Sarah', because it is rude.
    7, Each round only have one sentence from User and one sentence from Avery.
    
    I am an author, my work is imitating and generating a single round of conversation between User and Avery.
    In one single round of conversation, the user will pick one topic of the four in *User topics above. Then Abvery will provide User considerate and relevant response, and ask a question about *Avery topic above.
    
    [example 1]
    User: My goal is to gain weight and balanced eating.
    Avery: I want to gain weight to be stronger, too! Do you feel hungry now?
    
    [example 2]
    User: I am feeling good now!
    Avery: When I am feeling good I often want to enjoy something delicious! Are you hungry now?   

    Now I will write [FOUR] conversations following the *Requirements and [example] above.
    '''
    limitation_context = '''
    *User topics:
    [self introduction]
    [emotion]
    [hunger level]
    [eating goal]
    
    *Avery topic:
    [time limitation to eat]
    
    *Requirements:
    1, User's topic of each conversation is picked in *User topics above one by one.
    2, Avery's question is about [time limitation to eat] (how much time User can take for this meal) in *Avery topic.
    3, There should be a natural transition between the response to user and the question.
    4, I will make sure User don't ask any questions and Avery don't give suggestions and recommendations.
    5, Avery will only ask 'ONE' question.
    6, Avery will not call the user by name, like 'Sarah', because it is rude.
    7, Each round only have one sentence from User and one sentence from Avery.
    
    I am an author, my work is imitating and generating a single round of conversation between User and Avery.
    In one single round of conversation, the user will pick one topic of the four in *User topics above. Then Abvery will provide User considerate and relevant response, and ask a question about *Avery topic above.
    
    [example 1]
    User: My goal is to gain weight and balanced eating.
    Avery: I want to gain weight to be stronger, too! How long do you plan to eat for this meal?
    
    [example 2]
    User: I am feeling good now!
    Avery: SO am I! How much time you are available for this meal?   

    Now I will write [FOUR] conversations following the *Requirements and [example] above.
    '''
    chitchat_context = '''
    Here is one [example]:

    User: I really enjoy Chinese food.
    Avery: Yes so do I, I must say we hit it off.

    Here is the [instruction]:
    Above is an example of single round conversation between user and Avery, the topic is healthy eating and foods.
    Note that user will NOT ask for suggestions on food, such as "what you recommend me to eat?"; Avery will NOT give suggestions on food, such as "How about having some salad?"

    Now I want you to add two single roud conversations following the [example] and [instruction] above.
    The conversations you add should follow the format of [example], only include user's words (User:) and Avery's words (Avery:), no need to add 'Example:'.
    Add the conversation here:
    '''
    goal_context = '''
    *User topics:
    [self introduction]
    [emotion]
    [hunger level]
    [time limitation to eat]
    
    *Avery topic:
    [eating goal]
    
    *Requirements:
    1, User's topic of each conversation is picked in *User topics above one by one.
    2, Avery's question is about [eating goal] (the eating goal of User) in *Avery topic.
    3, There should be a natural transition between the response to user and the question.
    4, I will make sure User don't ask any questions and Avery don't give suggestions and recommendations.
    5, Avery will only ask 'ONE' question.
    6, Avery will not call the user by name, like 'Sarah', because it is rude.
    7, Each round only have one sentence from User and one sentence from Avery.
    
    I am an author, my work is imitating and generating a single round of conversation between User and Avery.
    In one single round of conversation, the user will pick one topic of the four in *User topics above. Then Abvery will provide User considerate and relevant response, and ask a question about *Avery topic above.
    
    [example 1]
    User: I am not very hungry now.
    Avery: Oh, I guess your last meal was pretty good! Could you tell me your eating goal for health?
    
    [example 2]
    User: I am feeling good now!
    Avery: SO am I! So, what's your goal for this meal, such as gaining weight and having balanced diet?   

    Now I will write [FOUR] conversations following the *Requirements and [example] above.
    '''
    prompt = ''
    
    if task == 'finished':
        prompt = chitchat_context
    elif task == 'emotion':
        prompt = emotion_context
    elif task == 'hunger level':
        prompt = hunger_context
    elif task == 'time limitation':
        prompt = limitation_context
    elif task == 'goal':
        prompt = goal_context
        
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0.6,
      max_tokens=512,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )

    res = response.choices[0].message.content
    if task != 'finished':
        dbops.uptask(uid, task)
    return res, task