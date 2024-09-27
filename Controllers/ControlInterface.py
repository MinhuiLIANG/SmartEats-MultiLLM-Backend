import openai
import sys 
sys.path.append("..") 
from Components import controller

def controlInterface(order, uid):
    return controller.controller(order, uid)