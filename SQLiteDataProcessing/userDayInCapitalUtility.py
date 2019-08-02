#!/usr/bin/python
# -*- coding: cp936 -*-

""" userDayInCapitalUtility.py
对db中usrDayInCapital表格进行数据处理
"""

import sqlite3

class userDayInCapitalUtility:

    '''
    拿到有效入金的用户以及其有效入金的时间
    @return: dictionary: {effectivekhcode: effectivecapticaldate}
    '''
    def geteffectiveCapitalUsersAndDates(self):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT * FROM usrDayInCapital WHERE zzc >= 1000'
            myDict = {}
            for date, khcode, zzc in db.execute(sqStatement):
                print(str(date))
                #按日期顺序遍历
                if khcode not in myDict:
                    myDict[str(khcode).strip()] = date

        return myDict

'''
u = userDayInCapitalUtility()
print(u.geteffectiveCapitalUsersAndDates())
'''