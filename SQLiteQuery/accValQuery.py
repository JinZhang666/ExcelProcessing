import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd


class accValQuery:

    def checkIfEffectiveCapital(self, khcode):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT iseffectivecapital, capitaldate FROM accval WHERE khcode = ?'
            for iseffecitvecapital, capitaldate in db.execute(sqStatement, [str(khcode).strip(),]):
                print('isEffectiveCapital: ', iseffecitvecapital[0])
                if iseffecitvecapital[0] == '1':
                    return capitaldate
                else:
                    if iseffecitvecapital[0] == '0':
                        return None
        return None

    def checkIfEffectiveLogin(self, khcode):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT iseffectivelogin, logindate FROM accval WHERE khcode = ?'
            for iseffectivelogin, logindate in db.execute(sqStatement, [str(khcode).strip(), ]):
                print('isEffectiveLogin: ', iseffectivelogin[0])
                if iseffectivelogin[0] == '1':
                    return logindate
                else:
                    if iseffectivelogin[0] == '0':
                        return None
        return None

    def checkIfEffectiveTrade(self, khcode):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT iseffectivetrade, tradedate FROM accval WHERE khcode = ?'
            for iseffectivetrade, tradedate in db.execute(sqStatement, [str(khcode).strip(), ]):
                print('iseffectivetrade: ', iseffectivetrade[0])
                if iseffectivetrade[0] == '1':
                    return tradedate
                else:
                    if iseffectivetrade[0] == '0':
                        return None
        return None


    def checkIfEffectiveATrade(self, khcode):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT iseffectiveatrade, atradedate FROM accval WHERE khcode = ?'
            for iseffectiveatrade, atradedate in db.execute(sqStatement, [str(khcode).strip(), ]):
                print('iseffectiveatrade: ', iseffectiveatrade[0])
                if iseffectiveatrade[0] == '1':
                    return atradedate
                else:
                    if iseffectiveatrade[0] == '0':
                        return None
        return None

'''
test = aTradeQuery()
print(test.checkIfEffectiveATrade('335000011709'))
print(test.checkIfEffectiveCapital('335000011709'))
print(test.checkIfEffectiveLogin('335000011709'))
print(test.checkIfEffectiveTrade('335000011709'))
'''

