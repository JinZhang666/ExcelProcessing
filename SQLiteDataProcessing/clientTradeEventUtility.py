#!/usr/bin/python
# -*- coding: cp936 -*-

""" clientTradeEventUtility.py
��db��clientTradeEvent���������ݴ���
"""

import sqlite3

class clientTradeEventUtility:

    '''
    �õ���Ч���׵��û��Լ�����Ч���׵�ʱ�䣨�������罻�׵���һ�죩
    @return: dictionary: {effectivekhcode: effectivetradedate}
    '''

    def geteffectiveTradeUsersAndDates(self):
        myDict = {}
        # ���� clienttradeevent ���������ͳ�Ƴ���Чtrade����
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, tradedate FROM clienttradeevent'
            for khcode, tradedate in db.execute(sqStatement):
                #������˳�����
                if str(khcode).strip() not in myDict:
                    myDict[str(khcode).strip()] = tradedate
        return myDict

#print(clientTradeEventUtility().geteffectiveTradeUsersAndDates())
