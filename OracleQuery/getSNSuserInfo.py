#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import pandas as pd
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#from SQLiteToExcel.getSheet6FromSQLite import *


"""
基于手机号查询它对应的wechatID(N视界平台的WECHAT id
"""
def getSNSuserWechatID(phoneDic):
    resultDic = {}
    #print('getting expandedWechatReferrer')
    with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
        cur = db.cursor()
        for user_phone in phoneDic:
            cur.execute(
                'SELECT phone, id, nick_name, real_name FROM sns_user_info WHERE phone =:1',
                (user_phone,))
            res = cur.fetchall()
            for phone, id, nick_name, real_name in res:
                print(phone, id, nick_name, real_name)
    return resultDic


def getSNSuserWechatIDByPerson(phone):
    #print('getting expandedWechatReferrer')
    with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
        cur = db.cursor()
        cur.execute(
                'SELECT phone, id, nick_name, real_name FROM sns_user_info WHERE phone =:1',
                (phone,))
        res = cur.fetchall()
        for phone, id, nick_name, real_name in res:
            print(phone, id, nick_name, real_name)


def getSNSuserWechatIDByPersonName(real_name):
    #print('getting expandedWechatReferrer')
    result = []
    with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
        cur = db.cursor()
        cur.execute(
                'SELECT phone, id, nick_name, real_name FROM sns_user_info WHERE real_name =:1',
                (real_name,))
        res = cur.fetchall()
        for phone, id, nick_name, real_name in res:
            print(real_name, phone, id, nick_name)
            return 1
    return None



# 取temp里彗星杯用户
hxb = []
f = open("temp1", encoding='utf-8')
f2 = f.readlines()
for line in f2:
    line = line.replace("\n", '')
    hxb.append(line)
print(hxb)
print(len(hxb))

# print
for name in hxb:
    result = getSNSuserWechatIDByPersonName(name)
    if result is None:
        print(name)
# 取这些人的id
#print(getSNSuserWechatID(hxb))