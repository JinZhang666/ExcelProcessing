import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd


class capitalQuery:

    """
    date : 20190731
    """
    def getZZCbyKHCodeAndDate(self, khcode, date):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT zzc FROM usrDayInCapital WHERE khcode = ? AND date = ?'
            for zzc in db.execute(sqStatement, [str(khcode).strip(), str(date).strip()]):
                return zzc

cq = capitalQuery()
print(cq.getZZCbyKHCodeAndDate(398000010812, 20190731)[0])
