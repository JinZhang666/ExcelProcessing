#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import xlrd
import xlwt
from SQLiteQuery.aTradeQuery import *
from SQLiteDataProcessing.userDayATradeUtility import  *
from SQLiteQuery.newAccountQuery import *
from SQLiteQuery.inertialTestersQuery import *

def getaTradeSheetFromSQLite():
    # 打开数据库连接以及需要使用的表格文档
    # open('sheet3_baseline.csv', 'rt',
    #        encoding='utf-8', newline='') as src,
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:

        workbookdes = xlwt.Workbook()
        dst1 = workbookdes.add_sheet('sheet1')
        dst2 = workbookdes.add_sheet('sheet2')
        dst3 = workbookdes.add_sheet('sheet3')

        aq = aTradeQuery()
        au = userDayATradeUtility()
        newAccount = newAccountQuery()


        # 拿到所有0621号（不包括0621),进行过阿尔法跟投的用户
        activeUsers = aq.getAllUsersATradeAfterDate('20190621')
        print('activeUsers:', activeUsers)

        # 拿到所有在0501 - 0621 期间（包括0501和0621）跟投的份数的统计
        aTradeNumbersDic = au.getAllUsersATradeNumbersDuring('20190501', '20190621')
        print('aTradeNumbersDic:', aTradeNumbersDic)

        # 拿到所有在0501 - 0621 期间（包括0501和0621）跟投的次数的统计
        aTradeTimesDic = au.getUsersATradeTimesDuring('20190501', '20190621')
        print('aTradeTimesDic:', aTradeTimesDic)

        # 拿到所有用户总跟投份数
        aTradeNumbersDicAll = au.getAllUsersATradeNumbers()
        print('aTradeNumbersDicAll: ', aTradeNumbersDicAll)

        # 拿到所有用户总跟投次数
        aTradeTimesDicAll = au.getAllUsersATradeTimes()
        print('aTradeTimesDicAll: ', aTradeTimesDicAll)

        # 拿到所有内部测试人员的手机号
        iq = inertialTestersQuery()
        inertialUsers = iq.getallInertialTestersMobile()

        # 拿到所有单次跟投数量大于10的用户
        aTradeSingleNumberGreater10 = aq.getAllATradeUsersTradeNumberGreaterThan(10)
        print('aTradeSingleNumberGreater10: ', aTradeSingleNumberGreater10)

        '''
        一、α波跟投用户
        1、选择持续跟投α波次数>=10次的用户5名
        2、选择单次跟投份数>=10份的用户3名
        3、选择20190501~20190621期间，跟投1次或2次即放弃的用户5名
        '''
        '''
        1
        '''
        ''''
        dst1.write(0, 0, '客户号')
        dst1.write(0, 1, '客户手机号')
        dst1.write(0, 2, '总跟投次数')

        row = 1
        for khcode in aTradeTimesDicAll:
            # 用户手机
            usrmobile = newAccount.getMobileByKHCode(khcode)
            if len(usrmobile) > 0:
                usrmobile = newAccount.getMobileByKHCode(khcode)[0].replace('(', '').replace(')', '').replace(',', '')
                usrmobile = str(usrmobile).strip()
            else:
                usrmobile = None
            # print(usrmobile)

            print(khcode)
            print(aTradeTimesDicAll[khcode])
            print("usrmobile in inertialUsers?:", usrmobile in inertialUsers)
            if (aTradeTimesDicAll[khcode] >= 10) and (usrmobile not in inertialUsers):
                dst1.write(row, 0, khcode)
                dst1.write(row, 1, usrmobile)
                dst1.write(row, 2, aTradeTimesDicAll[khcode])
                row = row + 1

        workbookdes.save('../output/aTradeResult.xls')
        '''

        '''
        3. 
        '''
        '''
        dst3.write(0, 0, '客户号')
        dst3.write(0, 1, '0501-0621跟投次数')
        dst3.write(0, 2, '0621后跟投否')

        row = 1
        for khcode in aTradeTimesDic:
            print(khcode, aTradeTimesDic[khcode] )
            if aTradeTimesDic[khcode] <= 2 and (khcode not in activeUsers):
                dst3.write(row, 0, khcode)
                dst3.write(row, 1, aTradeTimesDic[khcode])
                dst3.write(row, 2, '否')
                row = row + 1
        '''


        '''
        Sheet 2, 跟投数量大于10的用户
        '''
        '''
        dst2.write(0, 0, '客户号')
        dst2.write(0, 1, '客户手机号')
        dst2.write(0, 2, '总跟投份数')

        row = 1
        for khcode in aTradeNumbersDicAll:
            # 用户手机
            usrmobile = newAccount.getMobileByKHCode(khcode)
            if len(usrmobile) > 0:
                usrmobile = newAccount.getMobileByKHCode(khcode)[0].replace('(','').replace(')','').replace(',','')
                usrmobile = str(usrmobile).strip()
            else:
                usrmobile = None
            #print(usrmobile)

            print("usrmobile in inertialUsers?:", usrmobile in inertialUsers)
            if (aTradeNumbersDicAll[khcode] >= 10) and (usrmobile not in inertialUsers):
                dst2.write(row, 0, khcode)
                dst2.write(row, 1, usrmobile)
                dst2.write(row, 2, aTradeNumbersDicAll[khcode])
                row = row + 1
        '''


        '''
        Sheet 2, 单次跟投数量大于10的用户
        '''
        dst2.write(0, 0, '客户号')
        dst2.write(0, 1, '客户手机号')
        dst2.write(0, 2, '单次跟投份数')

        row = 1
        for khcode in aTradeSingleNumberGreater10:
            # 用户手机
            usrmobile = newAccount.getMobileByKHCode(khcode)
            if len(usrmobile) > 0:
                usrmobile = newAccount.getMobileByKHCode(khcode)[0].replace('(','').replace(')','').replace(',','')
                usrmobile = str(usrmobile).strip()
            else:
                usrmobile = None
            #print(usrmobile)

            #print("usrmobile in inertialUsers?:", usrmobile in inertialUsers)
            if usrmobile not in inertialUsers:
                dst2.write(row, 0, khcode)
                dst2.write(row, 1, usrmobile)
                dst2.write(row, 2, aTradeSingleNumberGreater10[khcode])
                row = row + 1

        workbookdes.save('../output/aTradeResult.xls')

getaTradeSheetFromSQLite()
