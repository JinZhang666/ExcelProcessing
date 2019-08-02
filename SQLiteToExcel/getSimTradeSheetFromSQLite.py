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
        topusers = sq.getTopSimTradeUsers(30) #���ؽ�������ǰ30����û��ֻ��ţ���Ϊ��Ҫ�޳��ڲ�������Ա

        iq = inertialTestersQuery()
        inertialUsers = iq.getallInertialTestersMobile()

        kcb = kcbActQuery()
        kcbtopUsers = kcb.getTopSimTradeUsers(30)

        '''
        ����ģ�⽻���û�
        1��N�ӽ�����˺ŵ�ʹ���û���ȡ������������ǰ10���û�(����ڲ���Ա��
        2���ƴ�������û���ȡ������������ǰ10���û�
        '''

        '''
        2
        '''
        dst2.write(0, 0, '�ƴ�������û�')
        dst2.write(0, 1, '��������')
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
        dst1.write(0, 0, 'ģ�⽻���û�')
        dst1.write(0, 1, 'ģ�⽻������')

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
