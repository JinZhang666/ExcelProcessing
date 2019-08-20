#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importTradeLogToSQLite():
    # SQLite中table的名字
    tableName = 'clienttradeevent'

    # 建立数据库的连接
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO ' + tableName + '(khcode, khqz, wtfs, tradedate, wtlb, zqdm, zqmc, wtsl, cjsl, wtgy,sbxw, czzd) ' \
                          'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

        # 清空的数据库遗留的数据（选择）
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\\trade\\tradelog.xlsx'
        sheetName = 'SQL Results'
        df = pd.read_excel(workbookPath, sheet_name=sheetName)

        """ 
        #当输入是一整个文件夹的所有文件的时候
        for root, dirs, files in os.walk(inputFolder):
            for file_ in files: 
                workbookPath = root + file_
                sheetName = os.path.splitext(file_)[0]
                df = pd.read_excel( workbookPath, sheetname = sheetName)
        """

        # 打印整张表的抬头
        print("df Column headings:")
        print(df.columns)

        # 打印摘取的某几列，确保字段顺序与SQL语句的字段顺序一一对应
        df1 = df[['KHH', 'KHQZ', 'WTFS', 'WTRQ', 'WTLB', 'ZQDM', 'ZQMC', 'WTSL', 'CJSL', 'WTGY', 'SBXW', 'CZZD']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)

        """
        # 转变某一列的类型
        df1['OperateTime'] = df1['OperateTime'].astype('str')
        """

        try:
            print('3')
            db.executemany(insert_template, df1.values)
        except sqlite3.Error as e:
            print('2')
            print(e)
            db.rollback()
        else:
            db.commit()

        # 检查是不是所有的数据都被加载了
        select_stmt = 'SELECT khcode FROM ' + tableName + ';'
        row = 0
        for khcode in db.execute(select_stmt).fetchall():
            print(str(khcode))
            row = row + 1
        print("row number: ", row)

#importTradeLogToSQLite()
