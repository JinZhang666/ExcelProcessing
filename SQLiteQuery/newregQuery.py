import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

class newregQuery:

    def getWechatReferRelation(khusrmoblie):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            sqStatement = 'SELECT refid, refnickname, refrealname, refphone, pageindex FROM newreg' \
                          'WHERE newreg.usrmobile = ?'

            wechatRefArray = db.execute(sqStatement, [khusrmoblie,])
            return wechatRefArray