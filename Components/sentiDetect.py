from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

def senti_interface(uid):
  
    sentiPrompt = '''Please analyze the sentiment in <sentence>. There are some examples to look at. 
    Your answer in <Emotion> should be positive, negative, or neutral.
    Examples:
    <sentence>: I'm too busy to eat anything during the daytime and felt hungry during the night.
    <Emotion>: negative
    
    <sentence>: Eating healthy makes me feel good.
    <Emotion>: positive
    
    <sentence>: '''
    
    client = OpenAI(api_key = "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")

    sentence = dbops.getlastusersent(uid)
    interface = "\n<Emotion>:"
    prompt = sentiPrompt + sentence + interface
    
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
    return res
