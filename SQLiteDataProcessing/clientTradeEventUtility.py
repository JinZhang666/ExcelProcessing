#!/usr/bin/python
# -*- coding: cp936 -*-

""" clientTradeEventUtility.py
对db中clientTradeEvent表格进行数据处理
"""

import sqlite3

class clientTradeEventUtility:

    '''
    拿到有效交易的用户以及其有效交易的时间（进行最早交易的那一天）
    @return: dictionary: {effectivekhcode: effectivetradedate}
    '''

    def geteffectiveTradeUsersAndDates(self):
        myDict = {}
        # 基于 clienttradeevent 里面的数据统计出有效trade的人
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, tradedate FROM clienttradeevent'
            for khcode, tradedate in db.execute(sqStatement):
                #按日期顺序遍历
                if str(khcode).strip() not in myDict:
                    myDict[str(khcode).strip()] = tradedate
        return myDict

#print(clientTradeEventUtility().geteffectiveTradeUsersAndDates())
