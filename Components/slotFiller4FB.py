from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

uid = 'asdkhasd'
def fb_interface():
    client = OpenAI(api_key = "your_api_key")
    
    slot_prompt = '''
    topic 1: <emotion> -> values 1: [<positive>, <neutral>, <negative>]
    topic 2: <hunger level> -> values 2: [<starving>, <neutral>, <satisfied>]
    topic 3: <time limitation> -> value 3: [<limited>, <neutral>, <sufficient>]

    Above pairs show the map of topics and values, each topic (such as <emotion>) relates to several values (<positive>, <neutral>, <negative>).
    There will be a feed back passage from the User, please first judge what topics listed above are mentioned by User, then analyze the user's intent or attitudes towards the topic.

    Here are two examples:
    User: I am busy I don't have time to eat it.
    Your output: <time limitation>:<limited>

    User: This one is too mushy, no appetite.
    Your output: <hunger level>:<satisfied>

    First you need to judge what is the topic according to User's words. In the first example, 'I am busy I don't have time to eat it' indicates the topic is <time limitation>;
    in te second example, 'This one is too mushy, no appetite', the topic is <hunger level>.
    Second you need to judge what is User's intent, or attitudes related to the topic you just find according to User's words. In the first example, 'busy', 'don't have time' means the <time limitation> is <limited>,so the output is <time limitation>:<limited>; in the second example, 'This one is too mushy, no appetite' means User is not very hungry, so the output is <hunger level>:<satisfied>.
    So your output of first example is: <time limitation>:<limited>; for your second example, it is <hunger level>:<satisfied>.

    Now try this feedback:\n
    '''
    
    interface = '\nYour output: '
    sent = dbops.getlastusersent(uid)
    prompt = slot_prompt + sent + interface
    
    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0,
      max_tokens=20,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )
    res = response.choices[0].message.content
    return res
  
def profile_editor():
  res = fb_interface()
  lst = res.split(':')
  topic_list = ['emotion', 'hunger level', 'time limitation']
  value_list = ['positive', 'neutral', 'negative', 'limited', 'sufficient', 'starving', 'satisfied']
  if len(lst) > 1:
    topic = lst[0].replace('<','').replace('>','')
    value = lst[1].replace('<','').replace('>','')
    if topic in topic_list and value in value_list:
      if topic == 'emotion':
        dbops.upemo(uid, value)
      if topic == 'hunger level':
        dbops.uphunger(uid, value)
      if topic == 'time limitation':
        dbops.uplimit(uid, value)