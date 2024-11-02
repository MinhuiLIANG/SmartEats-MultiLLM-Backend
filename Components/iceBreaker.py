from openai import OpenAI
import sys

sys.path.append("..")
from Components import paraphraser
from DAO import dbops


# get it from frontend
# uid = "asdkhasd"
def iceBreak_interface(uid):
    res = "I am SmartEats, a nutrition expert here to provide personalized dietary recommendations for you.\n\nIn this conversation, we'll delve into your basic information, dietary preferences, lifestyle, and health goals. I will ask you several questions to collect the information and provide nutritional suggestions based on your responses. After that, I'll try to search for some food that meet your needs. Ready to start?"
    return res