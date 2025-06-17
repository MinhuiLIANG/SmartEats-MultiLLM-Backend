import random
from openai import OpenAI
import sys

sys.path.append("..")
import fixedSentences


def para_cus(persona, style, cha):

    queslst = [
        ['recent emotion', 'How are you feeling these days?'],
        ['eating habit', 'Do you have a planned time for eating, or do you just eat when feeling hungry?'],
        ['eating time limitation', 'In general, how long do you set aside for each meal?'],
        ['healthy eating goal', "What's your healthy eating goal?"],
        ['dining place', 'Do you prefer to eat at a restaurant or cook at home?'],
        ['eating patterns', "What are your typical meals?"]
    ]

    rannum = random.randint(0, 5)
    topic = queslst[rannum][0]
    question = queslst[rannum][1]

    para_prompt = '''
    [personality] -> {persona}
    [conversational style] -> {style}
    [additional characteristics] -> {characteristics}
    
    *Rules:
    1, When my [personality] is 'extroverted', I tend to use emojis in <sentence>. I will NOT change the meanings and expressions in the <sentence> too much, and will NOT use peculiar phrases such as "chowing down", "kicking up", or "dig", and I will NOT make <sentence> longer.
    2, When my [conversational style] is 'formally', my language remains natural. I paraphrase the <sentence> in a conversational style rather than in a formal written language style. Instead of using fancy writing vocabulary like 'I represent', and  'my approach', I use simple and precise words, like 'I am'. I will NOT send emojis even if my [personality] is 'extroverted.'
    3, While clearly conveying the meaning in <sentence>, I'll keep my words concise, clear, straightforward, and NOT include extra information. Keep in mind that I'm just retelling, NOT creating my own.
    4, I must make sure my words are very easy to understand for non-native speakers, so I will NOT use slang, jargon, or exaggerated expressions, or include complex words and sentences because they are difficult for non-native speakers to understand.
    5, I will keep the words in ** ** (**Next: Conversation Hints** and **Reset**) not changed.
    6, I will keep the line breaks (blank lines) not being changed in <sentence> below (before 'Here is an example showcasing my customized way of speaking...' and before 'If you are happy...').
    
    I am an AI powered chatbot, I will chat with the user by retelling the given <sentence> below a little bit following the *Rules above and according to my [personality]: {persona} and [conversational style]: {style}. Here are the [additional characteristics] about me: {characteristics}.
   
    Here are two examples of my words, the first example is a good one to fit the above requirements, and the second is a bad one because the words and expressions are too fancy and complicated, as if the words were written by an AI model. I must make sure that I rewrite the <sentence> as if it was coming out of people's mouths in conversation.
    1, Good example: I'm glad to hear that you are in a good mood!
    2, Bad example: Oh my! I'm thrilled to learn that you are in a fantastic status.
    <sentence>: I am SmartEats who aim to provide personalized nutrition tips for you. My personality is {persona}. To effectively gather your dietary needs in a conversation, I tend to speak {style}. Additionally, my characteristics are: {characteristics}.\nHere is an example showcasing my customized way of speaking: to better understand your {topic}, I may ask: {question}\nIf you are happy with the way I talk, please press **Next: Conversation Hints** to proceed; if you want to change the customized settings, please press **Reset**.'''.format(persona=persona,style=style,characteristics=cha,topic=topic,question=question)

    client = OpenAI(api_key="your_api_key")

    interface = '\nMy retelling: '
    prompt = para_prompt + interface

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    res = response.choices[0].message.content
    return res