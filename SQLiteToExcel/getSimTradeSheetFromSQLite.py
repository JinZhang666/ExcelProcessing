#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import xlrd
import xlwt
from SQLiteQuery.simTradeQuery import *
from SQLiteQuery.inertialTestersQuery import *
from SQLiteQuery.kcbActQuery import *

def getSimTradeSheetFromSQLite():

    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:

        workbookdes = xlwt.Workbook()
        dst1 = workbookdes.add_sheet('sheet1')
        dst2 = workbookdes.add_sheet('sheet2')

        sq = simTradeQuery()
        topusers = sq.getTopSimTradeUsers(30) #返回交易天数前30多的用户手机号，因为还要剔除内部测试人员

        iq = inertialTestersQuery()
        inertialUsers = iq.getallInertialTestersMobile()

        kcb = kcbActQuery()
        kcbtopUsers = kcb.getTopSimTradeUsers(30)

        '''
        三、模拟交易用户
        1、N视界仿真账号的使用用户，取交易天数最多的前10名用户(提出内部人员）
        2、科创板大赛用户，取交易天数最多的前10名用户
        '''

        '''
        2
        '''
        dst2.write(0, 0, '科创版大赛用户')
        dst2.write(0, 1, '交易天数')
        finalTopUsers = {}
        count = 0
        row = 1
        for mobilephone in kcbtopUsers:
            if (mobilephone not in inertialUsers) and (mobilephone not in finalTopUsers):
                finalTopUsers[mobilephone] = kcbtopUsers[mobilephone] #tradedays
                dst2.write(row, 0, mobilephone)

                dst2.write(row, 1, kcbtopUsers[mobilephone])
                count = count + 1
                row = row + 1
            else:
                print(mobilephone, "is inertialUsers!")
            if count == 10:
                break
        workbookdes.save('../output/simTradeResult.xls')

        '''
        1
        '''
        '''
        dst1.write(0, 0, '模拟交易用户')
        dst1.write(0, 1, '模拟交易天数')

        finalTopUsers = {}
        count = 0
        row = 1
        for mobilephone in topusers:
            if (mobilephone not in inertialUsers) and (mobilephone not in finalTopUsers):
                finalTopUsers[mobilephone] = topusers[mobilephone] #tradedays
                dst1.write(row, 0, mobilephone)
                dst1.write(row, 1, topusers[mobilephone])
                count = count + 1
                row = row + 1
            else:
                print(mobilephone, "is inertialUsers!")
            if count == 10:
                break
        '''




getSimTradeSheetFromSQLite()
