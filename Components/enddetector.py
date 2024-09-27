from openai import OpenAI
import sys 
sys.path.append("..") 
from DAO import dbops

#uid = "asdkhasd"
def end_interface(uid):
    sent = dbops.getlastusersent(uid).replace("user:","")

    detPrompt = '''
    <response>: {sent}
    Above is a response from user after he/she is recommended some food. Please analyze if the user accept the recommendation.
    Your output should be [yes] or [no]. [yes] means the user accept the recommendation, [no] means the user reject the recommendation.
    Your output:
    '''.format(sent = sent) 
    
    client = OpenAI(api_key = "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")
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": detPrompt}
      ],
      temperature=0,
      max_tokens=6,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )
    res = response.choices[0].message.content.strip('[').strip(']')
    return res