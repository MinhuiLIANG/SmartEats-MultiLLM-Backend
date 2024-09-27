import sys

sys.path.append("..")
import fixedSentences
from DAO import dbops
from Components import upgrade_endtip


# uid = "asdkhasd"
def EndOne(uid):
    dbops.upaccfrst(uid, "True")
    res = fixedSentences.prefixes["end1"]

    tip = upgrade_endtip.getips(uid)
    sent = res + '\n\nAnd, ' + tip

    dbops.upconversation_b(uid, sent)
    return {'endone': sent}
