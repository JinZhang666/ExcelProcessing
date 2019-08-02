import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

class newAccountQuery:

    # 返回所有对应的营销人员已离职的用户
    # isLeftMarketPer字段是sheet2运算出的结果
    def getAllLeftMarketPersUsers(self):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode FROM newaccount WHERE isLeftMarketPer is not NULL'
            allLeftMarketPerUsers = []
            for khcode in db.execute(sqStatement):
                allLeftMarketPerUsers.append(str(khcode))
            return allLeftMarketPerUsers

    #根据用户的手机号拿到用户的客户号
    def getKHCodeByMobile(self, singleMobileNuber):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khcode FROM newaccount WHERE usrmobile = ?'
            result = []
            for khcode in db.execute(sqStatement, [singleMobileNuber, ]):
                result.append(str(khcode))
            return result

    #根据用户的客户号拿到用户的手机号
    def getMobileByKHCode(self, khcode):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT khusrmobile FROM newaccount WHERE khcode = ?'
            result = []
            for khusrmobile in db.execute(sqStatement, [khcode, ]):
                result.append(str(khusrmobile))
            return result




