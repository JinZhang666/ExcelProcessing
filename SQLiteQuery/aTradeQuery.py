import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

# 返回所有对应的营销人员已离职的用户
class aTradeQuery:

    '''
    选择20190501~20190621
    期间，跟投1次或2次即放弃的用户5名
    '''

    '''
    找出所有在某一个日期之后有阿尔法跟投的用户
    日期格式： 20190621
    '''

    def getAllUsersATradeAfterDate(self, date):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate FROM usrdayatrade WHERE atradedate > ?'
            allUsersATradeAfterDate = []
            for khcode, atradedate in db.execute(sqStatement, [str(date).strip(),]):
                allUsersATradeAfterDate.append(str(khcode))
                print(khcode)
                print(atradedate)
            return allUsersATradeAfterDate

    '''
    @input: 数字
    @output: 客户号的数组
    '''
    def getAllATradeUsersTradeNumberGreaterThan(self, number):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode, atradedate, atradenumber FROM usrdayatrade WHERE atradenumber >= ?'
            usersKHCode = {}
            for khcode, atradedate, atradenumber in db.execute(sqStatement, [str(number).strip(),]):
                if (str(khcode).strip() != 'nan') and (str(khcode).strip() not in usersKHCode):
                    usersKHCode[str(khcode).strip()] = atradenumber
                    #print("aa:", khcode)
                    #print("aa:", atradenumber)
            return usersKHCode

'''
query = newAccountQuery()
result = query.getAllUsersATradeAfterDate('20190621')
print(result)
print(len(result))
'''