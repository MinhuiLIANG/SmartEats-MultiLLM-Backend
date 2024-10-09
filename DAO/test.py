import dbops

print(dbops.getlasttround("travisliangstuxjtueducn")[0])
print(' ')
print(dbops.getlasttround("travisliangstuxjtueducn")[1])

meta = dbops.getlasttround("travisliangstuxjtueducn")
sen1 = meta[0]
sen2 = meta[1]

lst1 = sen1.split('user: ')
Avery1 = lst1[0].replace('chatbot: ', '')
user1 = lst1[1]
av1 = str(Avery1)
us1 = str(user1)
conversation1 = 'chatbot: ' + av1 + '\n' + 'user: ' + us1

lst2 = sen2.split('user: ')
Avery2 = lst2[0].replace('chatbot: ', '')
user2 = lst2[1]
av2 = str(Avery2)
us2 = str(user2)
conversation2 = 'chatbot: ' + av2 + '\n' + 'user: ' + us2

conversation = conversation1 + '\n\n' + conversation2

print(conversation)