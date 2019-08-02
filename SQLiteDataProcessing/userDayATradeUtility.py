#!/usr/bin/python
# -*- coding: cp936 -*-

""" userDayATradeUtility.py
对db中usrdayatrade表格进行数据处理
"""

import sqlite3

class userDayATradeUtility:

    '''
    拿到有效交易的用户以及其有效交易的时间（进行最早交易的那一天）
    @return: dictionary: {effectivekhcode: effectivetradedate}
    '''

    def geteffectiveATradeUsersAndDates(self):
        myDict = {}
        # 基于 clienttradeevent 里面的数据统计出有效trade的人
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate FROM usrdayatrade'
            for khcode, atradedate in db.execute(sqStatement):
                print(khcode, atradedate)
                #按日期顺序遍历
                if str(khcode).strip() not in myDict:
                    myDict[str(khcode).strip()] = atradedate
        return myDict

    '''
    得出某一个时间段跟投过的用户的跟投次数（天数，一天的跟投算一次）  
    日期格式 ‘20190501' '20190621'
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
    得出某一个时间段跟投过的用户的跟投份数
    日期格式 ‘20190501' '20190621'
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
    得出用户所有的跟投次数（天数，一天算一次） 
    日期格式 ‘20190501' '20190621'
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
    得出用户所有的跟投份数
    日期格式 ‘20190501' '20190621'
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
