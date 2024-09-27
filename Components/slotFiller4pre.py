import sys 
sys.path.append("..") 
from DAO import dbops

#uid = 'asdkhasd'
def profile_editor(uid):
  sent = dbops.getlastusersent(uid).replace("user:","")
  dbops.upprefer(uid, sent)