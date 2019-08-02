import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

# 返回所有对应的营销人员已离职的用户
class simTradeQuery:


    '''
    1、N视界仿真账号的使用用户，取交易天数最多的前10名用户
    '''

    def getTopSimTradeUsers(self, topnumber):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT usrmobile, tradedays FROM simtrade ORDER By tradedays DESC'
            top = {}
            count = 0
            for usrmobile, tradedays in db.execute(sqStatement):
                print(usrmobile, tradedays)
                if str(usrmobile).strip() not in top:
                    top[str(usrmobile).strip()] = tradedays
                    count = count + 1
                if count == topnumber:
                    break
            return top

print(simTradeQuery().getTopSimTradeUsers(10))
