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

    # ȡӪҵ�����¿����û��У�������Ч��¼����Ч����������û�
    yyb = []
    f = open("source.txt", 'r')
    f1 = f.readlines()
    for line in f1:
        line = line.replace("\n", '')
        yyb.append(line)

    print(yyb)
    filteryyb = []

    # ȡ���������¿����û��У�������Ч��¼����Ч����������û�
    hlw = []
    f2 = open("source2.txt", 'r')
    f3 = f2.readlines()
    for line in f3:
        line = line.replace("\n", '')
        hlw.append(line)

    print(hlw)
    filterhlw = []

    # ��yyb ɸѡ����¼����>=15���û�
    for user in yyb:
        if user in dic:
            if dic[user] >= 15:
                filteryyb.append(user)


    # ��hlw ɸѡ����½����>=10���û�
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