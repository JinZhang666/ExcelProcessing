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

def addSheet6WechatReferrer():
    '''
    �õ�����wechat referrer��ϵ��sheet6��dataframe: df
    '''
    df = pd.read_excel('../output/ACC+VAL.xls', sheetname='ACC+VAL')
    print('df from VCC + VAL')
    df = df[['����ʱ��','�����˺�','�ͻ����','�����ֻ���',\
             '��Ч��Ͷ','��Ͷ����','��Ч��¼','��¼�·�',\
             '��Ч���','�������','��Ч����','��������',\
             '��ֵ','��ز�����','��ز�����','Ӫ���˱���',\
             'Ӫ��������','Ӫ�������','Ӫ�����ֻ�','Ӫ��������',\
             'Ӫ��������','����','��ְ','���º��']]

    df['��¼�·�'] = df['��¼�·�'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')
    # df1['OperateTime'] = df1['OperateTime'].astype('str')

    '''
    ����getwechatreferrer�ó���dictionary
    directory�ṹ���û��ֻ��� + wechat referrer ��Ϣ
    { 13003278253 {'REFERRER_ID': '274c5d4788f945878371a8ac71d5d30a', '����id': '01', 'NICK_NAME': '�ܷ�', 'REAL_NAME': '�ܷ�', 'PHONE': '13813555536'} } 
    '''
    myDic = getWechatReferrer(df).getFinalResult()
    for user_phone in myDic:
        print(user_phone, myDic[user_phone])

    print("total final record number: ", len(myDic))

    # ̧ͷ����
    workbookdes = xlwt.Workbook()
    dst = workbookdes.add_sheet('ACC+VAL')

    dst.write(0, 0, '����ʱ��')  # A
    dst.write(0, 1, '�����˺�')  # B
    dst.write(0, 2, '�ͻ����')  # C
    dst.write(0, 3, '�����ֻ���')  # D
    dst.write(0, 4, '��Ч��Ͷ')  # E
    dst.write(0, 5, '��Ͷ����')  # F
    dst.write(0, 6, '��Ч��¼')  # G
    dst.write(0, 7, '��¼�·�')  # H
    dst.write(0, 8, '��Ч���')  # I
    dst.write(0, 9, '�������')  # I
    dst.write(0, 10, '��Ч����')  # I
    dst.write(0, 11, '��������')  # I
    dst.write(0, 12, '��ֵ')  # I
    dst.write(0, 13, '��ز�����')  # I
    dst.write(0, 14, '��ز�����')  # I
    dst.write(0, 15, 'Ӫ���˱���')  # I
    dst.write(0, 16, 'Ӫ��������')  # I
    dst.write(0, 17, 'Ӫ�������')  # I
    dst.write(0, 18, 'Ӫ�����ֻ�')  # I
    dst.write(0, 19, 'Ӫ��������')  # I
    dst.write(0, 20, 'Ӫ��������')  # I
    dst.write(0, 21, '����')  # I
    dst.write(0, 22, '��ְ')  # I
    dst.write(0, 23, '���º��')  # I
    dst.write(0, 24, 'REFERRER_ID')
    dst.write(0, 25, 'NICK_NAME')  # I
    dst.write(0, 26, 'REAL_NAME')
    dst.write(0, 27, 'PHONE')  # I
    dst.write(0, 28, '����id')  # I



    r = 1
    for index, row in df.iterrows():
        c = 0
        for col_name in df.columns:
            dst.write(r, c, str(row[col_name]).strip())
            c = c + 1
        if row['�����ֻ���'] in myDic:
            dst.write(r, 24, myDic[row['�����ֻ���']]['REFERRER_ID'])
            dst.write(r, 25, myDic[row['�����ֻ���']]['NICK_NAME'])
            dst.write(r, 26, myDic[row['�����ֻ���']]['REAL_NAME'])
            dst.write(r, 27, myDic[row['�����ֻ���']]['PHONE'])
            dst.write(r, 28, myDic[row['�����ֻ���']]['����id'])
        r = r + 1

    workbookdes.save('../output/ACC+VAL+WECHAT.xls')

addSheet6WechatReferrer()