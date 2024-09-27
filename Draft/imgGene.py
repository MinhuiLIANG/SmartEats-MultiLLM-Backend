from openai import OpenAI
import sys 
sys.path.append("..") 
from Components import entityExtractor

def image2(food1, food2):
    client = OpenAI(api_key = "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")
    #foods = entityExtractor.extractor_interface(passage=passage)
    prompt = 'These are two foods: food1 -> {f1}, food2 -> {f2}, generate one image of the two foods, but do not mix the two together. Distinguish them with a clear line to differentiate between food1 and food2.'.format(f1 = food1, f2 = food2)
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    #quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    return image_url