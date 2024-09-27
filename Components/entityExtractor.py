from openai import OpenAI
 
def extractor_interface(passage):
    para_prompt = '''
    Please identify and extract all the names of food or dishes in the given [passage].
    For example, if [passage]: "I recommend you to eat fruit sandwich and spaghetti bolognese for lunch", your output should be "fruit sandwich and spaghetti bolognese".
    Don't separate complete food name, for example, fruit sandwich is a whole, do not output fruit and sandwich.
    If [passage] includes more than one food names, Connect them with "and". For example, in "I recommend you to eat fruit sandwich and spaghetti bolognese for lunch", your output should be "fruit sandwich and spaghetti bolognese".
    [passage]: 
    ''' 
  
    client = OpenAI(api_key = "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")
    interface = '\nYour output: '
    prompt = para_prompt + passage + interface
    
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0301",
      messages=[
        {"role": "system", "content": prompt}
      ],
      temperature=0,
      max_tokens=96,
      top_p=1,
      frequency_penalty=0,    
      presence_penalty=0
    )
    
    res = response.choices[0].message.content
    return res