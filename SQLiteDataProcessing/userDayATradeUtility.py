#!/usr/bin/python
# -*- coding: cp936 -*-

""" userDayATradeUtility.py
��db��usrdayatrade���������ݴ���
"""

import sqlite3

class userDayATradeUtility:

    '''
    �õ���Ч���׵��û��Լ�����Ч���׵�ʱ�䣨�������罻�׵���һ�죩
    @return: dictionary: {effectivekhcode: effectivetradedate}
    '''

    def geteffectiveATradeUsersAndDates(self):
        myDict = {}
        # ���� clienttradeevent ���������ͳ�Ƴ���Чtrade����
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate FROM usrdayatrade'
            for khcode, atradedate in db.execute(sqStatement):
                print(khcode, atradedate)
                #������˳�����
                if str(khcode).strip() not in myDict:
                    myDict[str(khcode).strip()] = atradedate
        return myDict

    '''
    �ó�ĳһ��ʱ��θ�Ͷ�����û��ĸ�Ͷ������������һ��ĸ�Ͷ��һ�Σ�  
    ���ڸ�ʽ ��20190501' '20190621'
    '''
    def getUsersATradeTimesDuring(selfs, startdate, enddate):
        myDict = {}
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate, atradenumber FROM usrdayatrade WHERE atradedate >= ? AND atradedate <= ?'
            print("getting atrade info during ", startdate, " to ", enddate, " ... ")
            for khcode, atradedate, atradenumber in db.execute(sqStatement, [startdate, enddate, ]):
                if str(khcode).strip() in myDict:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan' and atradenumber > 0:
                        myDict[str(khcode).strip()] = int(myDict[str(khcode).strip()]) + 1
                else:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan' and atradenumber > 0:
                        myDict[str(khcode).strip()] = 1
            return myDict


    '''
    �ó�ĳһ��ʱ��θ�Ͷ�����û��ĸ�Ͷ����
    ���ڸ�ʽ ��20190501' '20190621'
    '''
    def getAllUsersATradeNumbersDuring(self, startdate, enddate):
        myDict = {}
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate, atradenumber FROM usrdayatrade WHERE atradedate >= ? AND atradedate <= ?'
            print("getting atrade info during ", startdate, " to ", enddate, " ... ")
            for khcode, atradedate, atradenumber in db.execute(sqStatement, [startdate, enddate,]):
                #print(khcode, atradedate, atradenumber)
                if str(khcode).strip() in myDict:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan':
                        myDict[str(khcode).strip()] = int(myDict[str(khcode).strip()]) + int(atradenumber)
                else:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan':
                        myDict[str(khcode).strip()] = int(atradenumber)
        return myDict

    '''
    �ó��û����еĸ�Ͷ������������һ����һ�Σ� 
    ���ڸ�ʽ ��20190501' '20190621'
    '''
    def getAllUsersATradeTimes(self):
        myDict = {}
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate, atradenumber FROM usrdayatrade'
            print("getting users atrade times ... ")
            for khcode, atradedate, atradenumber in db.execute(sqStatement):
                #print(khcode, atradedate, atradenumber)
                if str(khcode).strip() in myDict:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan'and atradenumber > 0:
                        myDict[str(khcode).strip()] = int(myDict[str(khcode).strip()]) + 1
                else:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan' and atradenumber > 0:
                        myDict[str(khcode).strip()] = 1
        return myDict



    '''
    �ó��û����еĸ�Ͷ����
    ���ڸ�ʽ ��20190501' '20190621'
    '''
    def getAllUsersATradeNumbers(self):
        myDict = {}
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate, atradenumber FROM usrdayatrade'
            print("getting users atrade times ... ")
            for khcode, atradedate, atradenumber in db.execute(sqStatement):
                #print(khcode, atradedate, atradenumber)
                if str(khcode).strip() in myDict:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan':
                        myDict[str(khcode).strip()] = int(myDict[str(khcode).strip()]) + int(atradenumber)
                else:
                    if (khcode is not None) and (atradenumber is not None) and atradenumber != 'nan':
                        myDict[str(khcode).strip()] = int(atradenumber)
        return myDict



#print(userDayATradeUtility().getAllUsersATradeTimes())
#print(userDayATradeUtility().getAllUsersATradeTimesDuring('20190501', '20190621'))
#print(userDayATradeUtility().geteffectiveATradeUsersAndDates())
