from SQLiteQuery.newAccountQuery import *


# 取互联网拉新开户用户中，符合有效登录、有效入金条件的用户
khcodes = []
f2 = open("source3.txt", 'r')
f3 = f2.readlines()
for line in f3:
    line = line.replace("\n", '')
    khcodes.append(line)

#print(len(khcodes))

for khcode in khcodes:
    n = newAccountQuery()
    n.getMarketRelationByKHCode(khcode)
