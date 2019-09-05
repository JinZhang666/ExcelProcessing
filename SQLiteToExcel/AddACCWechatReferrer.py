#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import pandas as pd
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#from SQLiteToExcel.getSheet6FromSQLite import *
from OracleQuery.getWechatReferrer import *
import xlrd
import xlwt

def addACCWechatReferrer():
    '''
    拿到不含wechat referrer关系的sheet6的dataframe: df
    '''
    df = pd.read_excel('../input/newAcc.xlsx', sheetname='newAcc')
    print('df from VCC + VAL')
    df = df[['开户营业部', 'YYB', 'KHYYB',
             'KHH',	'KHJC',	'KHMC',	'SJ',
             'KHRQ', 'TJRSJ', '人员编号', '人员姓名', 'HR编号',
             '人员类别', '手机',	'营业部编号', '营业部名称',	'QDBM',
             '客户群组', '账户状态',	'账户状态备注']]


    # df1['OperateTime'] = df1['OperateTime'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')

    '''
    根据getwechatreferrer得出的dictionary
    directory结构：用户手机号 + wechat referrer 信息
    { 13003278253 {'REFERRER_ID': '274c5d4788f945878371a8ac71d5d30a', '海报id': '01', 'NICK_NAME': '周锋', 'REAL_NAME': '周锋', 'PHONE': '13813555536'} } 
    '''
    myDic = getWechatReferrer(df).getFinalResult()
    for user_phone in myDic:
        print(user_phone, myDic[user_phone])

    print("total final record number: ", len(myDic))

    # 抬头补充
    workbookdes = xlwt.Workbook()
    dst = workbookdes.add_sheet('ACC+VAL')

    ''' COPY '''
    '''
    dst.write(0, 0, '开户时间')  # A
    dst.write(0, 1, '交易账号')  # B
    dst.write(0, 2, '客户简称')  # C
    dst.write(0, 3, '开户手机号')  # D
    dst.write(0, 4, '有效跟投')  # E
    dst.write(0, 5, '跟投日期')  # F
    dst.write(0, 6, '有效登录')  # G
    dst.write(0, 7, '登录月份')  # H
    dst.write(0, 8, '有效入金')  # I
    dst.write(0, 9, '入金日期')  # I
    dst.write(0, 10, '有效交易')  # I
    dst.write(0, 11, '交易日期')  # I
    dst.write(0, 12, '价值')  # I
    dst.write(0, 13, '落地部代码')  # I
    dst.write(0, 14, '落地部名称')  # I
    dst.write(0, 15, '营销人编码')  # I
    dst.write(0, 16, '营销人名称')  # I
    dst.write(0, 17, '营销人类别')  # I
    dst.write(0, 18, '营销人手机')  # I
    dst.write(0, 19, '营销部代码')  # I
    dst.write(0, 20, '营销部名称')  # I
    dst.write(0, 21, '销户')  # I
    dst.write(0, 22, '离职')  # I
    dst.write(0, 23, '当月红包')  # I
    '''
    ''' Something new '''
    dst.write(0, 21, 'REFERRER_ID')
    dst.write(0, 22, 'NICK_NAME')  # I
    dst.write(0, 23, 'REAL_NAME')
    dst.write(0, 24, 'PHONE')  # I
    dst.write(0, 25, '海报id')  # I
    dst.write(0, 26, '推荐渠道')
    dst.write(0, 27, '推荐子渠道')

    r = 1
    for index, row in df.iterrows():
        c = 0
        for col_name in df.columns:
            dst.write(r, c, str(row[col_name]).strip())
            c = c + 1
        if row['开户手机号'] in myDic:
            dst.write(r, 24, myDic[row['开户手机号']]['REFERRER_ID'])
            dst.write(r, 25, myDic[row['开户手机号']]['NICK_NAME'])
            dst.write(r, 26, myDic[row['开户手机号']]['REAL_NAME'])
            dst.write(r, 27, myDic[row['开户手机号']]['PHONE'])
            dst.write(r, 28, myDic[row['开户手机号']]['海报id'])
            dst.write(r, 29, myDic[row['开户手机号']]['推荐渠道'])
        r = r + 1

    workbookdes.save('../output/ACCWECHATExpanded.xls')

addACCWechatReferrer()