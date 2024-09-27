import openai
import sys 
sys.path.append("..") 
from Components import sentiDetect


def SentInterface(uid):
    res = sentiDetect.senti_interface(uid)
    return {'sentiment':res}
