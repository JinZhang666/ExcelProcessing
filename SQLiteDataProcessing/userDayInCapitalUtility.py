#!/usr/bin/python
# -*- coding: cp936 -*-

""" userDayInCapitalUtility.py
��db��usrDayInCapital���������ݴ���
"""

import sqlite3

class userDayInCapitalUtility:

    '''
    �õ���Ч�����û��Լ�����Ч����ʱ��
    @return: dictionary: {effectivekhcode: effectivecapticaldate}
    '''
    def geteffectiveCapitalUsersAndDates(self):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT * FROM usrDayInCapital WHERE zzc >= 1000'
            myDict = {}
            for date, khcode, zzc in db.execute(sqStatement):
                print(str(date))
                #������˳�����
                if khcode not in myDict:
                    myDict[str(khcode).strip()] = date

        return myDict

'''
u = userDayInCapitalUtility()
print(u.geteffectiveCapitalUsersAndDates())
'''