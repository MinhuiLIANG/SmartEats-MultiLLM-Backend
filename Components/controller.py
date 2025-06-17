from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

#uid = 'asdkhasd'
def controller(order, uid):
    currtopic = dbops.gettopic(uid)
    conv = dbops.getwholeconversation(uid)
    controllerprompt = '''
    [current topic] -> {topic}
    [actions] -> [<down>, <keep>]
    
    *Rules*:
    1. Most important: if [current topic] is not 'chitchat', you must select <down> in [actions]; you CANNOT select <keep> when [current topic] is not 'chitchat'.
    2. However, unlike in 1, if [current topic] is 'chitchat', you can select <down> or <keep> in [actions] as the current action. The guidelines for selecting an appropriate [current topic] are described in 3.
    3. If [current topic] is 'chitchat', you need to detect the user's intention. If you believe the user does not enjoy the conversation (e.g., responding with only a few words or random letters, not answering the question, or showing boredom), you need to select <down> in [actions]. On the contrary, if you believe the user is enjoying the conversation, keep engaging the user by actively talking to them and selecting <keep> in [actions].
    You are the topic manager of a conversation. Given the [current topic] above and *Conversation* below, you need to select an action from the above [actions], either <down> or <keep>, where <down> means switch to another topic and <keep> means keep or stay on the current topic, following the above *Rules*. 
    Note that you must ensure that if [current topic] is not chitchat, you can only select <down>.
    *Conversation*:
    {conv}
    '''.format(topic=currtopic, conv=conv)
    
    client = OpenAI(api_key = "your_api_key")

    interface = "\Your selection:"
    prompt = controllerprompt + interface
    
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0,
      max_tokens=10,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )  

    res = response.choices[0].message.content
    if order != 'none':
        res = order
    return res
