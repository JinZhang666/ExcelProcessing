#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3 
import pandas as pd

def importSimTradeToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            insert_template = "INSERT INTO simtrade " \
                    "(usrmobile, createtime, tradedays) " \
                     "VALUES (?, ?, ?);"

            db.execute('DELETE FROM simtrade;')

            df = pd.read_excel('..\input\simTrade.xlsx', sheetname='仿真用户')
            df1 = df[['手机号','注册日期','交易天数']]
            print(df1)

            # 转变某一列的类型
            df1['手机号'] = df1['手机号'].astype('str')
            df1['注册日期'] = df1['注册日期'].astype('str')
            df1['交易天数'] = df1['交易天数'].astype('str')

            try:
                print('3')
                db.executemany(insert_template, df1.values)
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback()
            else:
                db.commit()

            select_stmt = 'SELECT DISTINCT usrmobile FROM simtrade;'
            number = 0
            for row in db.execute(select_stmt).fetchall():
                print(str(row))
                number = number + 1

            print(number)
importSimTradeToSQLite()
