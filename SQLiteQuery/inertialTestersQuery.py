import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

# 返回所有对应的营销人员已离职的用户
class inertialTestersQuery:

    '''
    选择20190501~20190621
    期间，跟投1次或2次即放弃的用户5名
    '''

    '''
    找出所有在某一个日期之后有阿尔法跟投的用户
    日期格式： 20190621
    '''

    # ['13917035937'...]
    def getallInertialTestersMobile(self):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT mobile FROM inertialtesters'
            allInertialTesters = []
            for mobile in db.execute(sqStatement):
                allInertialTesters.append(str(mobile).replace('(','').replace(')','').replace('\'','').replace(',',''))
                print(mobile)
        return allInertialTesters

#query = inertialTestersQuery()
#result = query.getallInertialTestersMobile()
#print(result)
