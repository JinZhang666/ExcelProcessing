#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

def playground3():
    workbookPathZ = '..\input\Z.xlsx'
    workbookPathW = '..\input\W.xlsx'
    sheetNameZ = 'z'
    sheetNameW = 'w'
    dfZ = pd.read_excel(workbookPathZ, sheet_name=sheetNameZ)
    dfW = pd.read_excel(workbookPathW, sheet_name=sheetNameW)

    dfZ['MOBILENO'] = dfZ['MOBILENO'].astype('str')
    dfW['�ֻ���'] = dfW['�ֻ���'].astype('str')


    # ��ӡժȡ��ĳ���У�ȷ���ֶ�˳����SQL�����ֶ�˳��һһ��Ӧ
    dfz = dfZ['MOBILENO'].values
    dfw = dfW['�ֻ���'].values

    print(dfz.size)
    print(dfw.size)

    count = 0

    for numberz in dfz:
        print('dfz', numberz)

    for numberw in dfw:
        print('dfw', numberw)

    for n in dfz:
        if n not in dfw:
            print(n)
            count = count + 1
            #print(number)

    print(count)


playground3()