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
    # �����ݿ������Լ���Ҫʹ�õı���ĵ�
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


        # �õ�����0621�ţ�������0621),���й���������Ͷ���û�
        activeUsers = aq.getAllUsersATradeAfterDate('20190621')
        print('activeUsers:', activeUsers)

        # �õ�������0501 - 0621 �ڼ䣨����0501��0621����Ͷ�ķ�����ͳ��
        aTradeNumbersDic = au.getAllUsersATradeNumbersDuring('20190501', '20190621')
        print('aTradeNumbersDic:', aTradeNumbersDic)

        # �õ�������0501 - 0621 �ڼ䣨����0501��0621����Ͷ�Ĵ�����ͳ��
        aTradeTimesDic = au.getUsersATradeTimesDuring('20190501', '20190621')
        print('aTradeTimesDic:', aTradeTimesDic)

        # �õ������û��ܸ�Ͷ����
        aTradeNumbersDicAll = au.getAllUsersATradeNumbers()
        print('aTradeNumbersDicAll: ', aTradeNumbersDicAll)

        # �õ������û��ܸ�Ͷ����
        aTradeTimesDicAll = au.getAllUsersATradeTimes()
        print('aTradeTimesDicAll: ', aTradeTimesDicAll)

        # �õ������ڲ�������Ա���ֻ���
        iq = inertialTestersQuery()
        inertialUsers = iq.getallInertialTestersMobile()

        # �õ����е��θ�Ͷ��������10���û�
        aTradeSingleNumberGreater10 = aq.getAllATradeUsersTradeNumberGreaterThan(10)
        print('aTradeSingleNumberGreater10: ', aTradeSingleNumberGreater10)

        '''
        һ��������Ͷ�û�
        1��ѡ�������Ͷ��������>=10�ε��û�5��
        2��ѡ�񵥴θ�Ͷ����>=10�ݵ��û�3��
        3��ѡ��20190501~20190621�ڼ䣬��Ͷ1�λ�2�μ��������û�5��
        '''
        '''
        1
        '''
        ''''
        dst1.write(0, 0, '�ͻ���')
        dst1.write(0, 1, '�ͻ��ֻ���')
        dst1.write(0, 2, '�ܸ�Ͷ����')

        row = 1
        for khcode in aTradeTimesDicAll:
            # �û��ֻ�
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
        dst3.write(0, 0, '�ͻ���')
        dst3.write(0, 1, '0501-0621��Ͷ����')
        dst3.write(0, 2, '0621���Ͷ��')

        row = 1
        for khcode in aTradeTimesDic:
            print(khcode, aTradeTimesDic[khcode] )
            if aTradeTimesDic[khcode] <= 2 and (khcode not in activeUsers):
                dst3.write(row, 0, khcode)
                dst3.write(row, 1, aTradeTimesDic[khcode])
                dst3.write(row, 2, '��')
                row = row + 1
        '''


        '''
        Sheet 2, ��Ͷ��������10���û�
        '''
        '''
        dst2.write(0, 0, '�ͻ���')
        dst2.write(0, 1, '�ͻ��ֻ���')
        dst2.write(0, 2, '�ܸ�Ͷ����')

        row = 1
        for khcode in aTradeNumbersDicAll:
            # �û��ֻ�
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
        Sheet 2, ���θ�Ͷ��������10���û�
        '''
        dst2.write(0, 0, '�ͻ���')
        dst2.write(0, 1, '�ͻ��ֻ���')
        dst2.write(0, 2, '���θ�Ͷ����')

        row = 1
        for khcode in aTradeSingleNumberGreater10:
            # �û��ֻ�
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
