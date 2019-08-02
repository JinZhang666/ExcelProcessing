#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import xlrd
import xlwt
from SQLiteDataProcessing.userDayATradeUtility import *
from SQLiteQuery.inertialTestersQuery import *
from SQLiteQuery.newAccountQuery import *

def playground2():
    aTrade = userDayATradeUtility()
    dic1 = aTrade.getUsersATradeTimesDuring("20190501", "20190621")
    print (dic1)
    dic2 = aTrade.getUsersATradeTimesDuring("20190622","20190801")
    users1 = []
    inertialTesters = inertialTestersQuery().getallInertialTestersMobile()
    naq = newAccountQuery()

    # 取那些在0501 - 0621 期间登录1-2次的人
    for user in dic1:
        if dic1[user] <= 2:
            users1.append(user)

    # 确保他们在0621 之后没有登录
    for user in users1:
        if user not in dic2:
            usrmobile = None
            if len(naq.getMobileByKHCode(user)) > 0:
                usrmobile = naq.getMobileByKHCode(user)[0].replace('(', '').replace(')', '').replace(',', '')
                #print(usrmobile)
            if str(usrmobile).strip() in inertialTesters:
                print("usermobile is an inertial tester.")
            else:
                #print(user)
                #print(usrmobile)
                print(dic1[user])

playground2()