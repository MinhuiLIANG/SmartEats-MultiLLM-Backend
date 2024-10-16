from openai import OpenAI
import sys

sys.path.append("..")
from Components import paraphraser
from DAO import dbops


# get it from frontend
# uid = "asdkhasd"
def iceBreak_interface(uid):
    res = "I am SmartEats, a nutrition expert here to provide personalized dietary recommendations for you.\n\nIn this conversation, we'll delve into your basic information, dietary preferences, lifestyle, and health goals. I will ask you several questions to collect the information before recommending foods. After that, I'll try to search for some food that meet your needs and see if you would like to try them out in the upcoming week. Ready to start?"
    return res