import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

# 返回所有对应的营销人员已离职的用户
class kcbActQuery:
    '''
    科创版大赛的使用用户，取交易天数最多的前10名用户
    '''

    def getTopSimTradeUsers(self, topnumber):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT usrmobile, tradecode, tradedays FROM kcbactsimtrade ORDER BY tradedays DESC'
            top = {}
            count = 0
            for usrmobile, tradecode, tradedays in db.execute(sqStatement):
                print(usrmobile, tradecode, tradedays)
                if str(usrmobile).strip() not in top:
                    top[str(usrmobile).strip()] = tradedays
                    count = count + 1
                if count == topnumber:
                    break
            return top

print(kcbActQuery().getTopSimTradeUsers(10))