import sys

sys.path.append("..")
import fixedSentences
from DAO import dbops
from Components import endtip


# uid = "asdkhasd"
def EndOne(uid):
    dbops.upaccfrst(uid, "True")
    res = fixedSentences.prefixes["end1"]

    tip = endtip.getips(uid)
    sent = res + '\n\nAnd, ' + tip

    dbops.upconversation_b(uid, sent)
    return {'endone': sent}
