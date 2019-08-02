#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import xlrd
import xlwt
from SQLiteQuery.newAccountQuery import *
from SQLiteDataProcessing.clientLoginEventUtility import *
from SQLiteQuery.inertialTestersQuery import *

def playground():
    naq = newAccountQuery()
    inertialtesters = inertialTestersQuery().getallInertialTestersMobile()
    dic = clientLoginEventUtility().getTotalLogginDays()
    print(inertialtesters)

    # 取营业部拉新开户用户中，符合有效登录、有效入金条件的用户
    yyb = []
    f = open("source.txt", 'r')
    f1 = f.readlines()
    for line in f1:
        line = line.replace("\n", '')
        yyb.append(line)

    print(yyb)
    filteryyb = []

    # 取互联网拉新开户用户中，符合有效登录、有效入金条件的用户
    hlw = []
    f2 = open("source2.txt", 'r')
    f3 = f2.readlines()
    for line in f3:
        line = line.replace("\n", '')
        hlw.append(line)

    print(hlw)
    filterhlw = []

    # 从yyb 筛选出登录天数>=15的用户
    for user in yyb:
        if user in dic:
            if dic[user] >= 15:
                filteryyb.append(user)


    # 从hlw 筛选出登陆天数>=10的用户
    for user in hlw:
        if user in dic:
            if dic[user] >= 10:
                filterhlw.append(user)


    f5 = open("desyyb.txt", "w+")
    f6 = open("deshlw.txt", "w+")
    for user in filteryyb:
        usrmobile = None
        if len(naq.getMobileByKHCode(user)) > 0:
            usrmobile = naq.getMobileByKHCode(user)[0].replace('(','').replace(')','').replace(',','')
        #print(usrmobile)
        if str(usrmobile) in inertialtesters:
            print("usermobile is an inertial tester.")
        else:
            #f5.write("%s  "%user)
            #f5.write("%s  " %usrmobile)
            f5.write(str(dic[user]))
            f5.write("\n")
    for user in filterhlw:
        usrmobile = None
        if len(naq.getMobileByKHCode(user)) > 0:
            usrmobile = naq.getMobileByKHCode(user)[0].replace('(','').replace(')','').replace(',','')
        if str(usrmobile) in inertialtesters:
            print("usermobile is an inertial tester.")
        else:
            #f6.write("%s  "%user)
            #f6.write("%s  " %usrmobile)
            f6.write(str(dic[user]))
            f6.write("\n")

playground()