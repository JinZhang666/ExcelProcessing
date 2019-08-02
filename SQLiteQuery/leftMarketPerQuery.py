import sqlite3
import csv
import xlrd
import xlwt


def getAllLeftMarketPerIDs():
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        sqStatement = 'SELECT marketcode FROM leftmarketper'
        allLeftMarketPerIDs = []
        for marketcode in db.execute(sqStatement):
            allLeftMarketPerIDs.append(str(marketcode))
        return allLeftMarketPerIDs