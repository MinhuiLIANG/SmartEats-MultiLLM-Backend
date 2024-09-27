import openai
import sys 
sys.path.append("..") 
from Upgrades import intentdetection

def controlInterface(uid):
    sig = intentdetection.intentdetection(uid)
    print('topic of next question: ', sig)
    if sig == 'OK':
        return '<down>'
    else:
        return '<keep>'