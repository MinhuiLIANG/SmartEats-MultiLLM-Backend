import sys 
sys.path.append("..") 
import fixedSentences
from DAO import dbops


def FeedbackInterface(uid):
    res = fixedSentences.prefixes["fb"]
    dbops.upconversation_b(uid, res)
    return {'fb':res}