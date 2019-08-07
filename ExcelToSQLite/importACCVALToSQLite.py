#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os

def importAccValToSQLite():
    # SQLite中table的名字
    tableName = 'accval'

    # 建立数据库的连接
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO ' + tableName + '(khcode, iseffectivecapital, capitaldate, ' \
                                                       'iseffectivelogin, logindate, ' \
                                                       'iseffectivetrade, tradedate, ' \
                                                       'iseffectiveatrade, atradedate)' \
                          'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'

        # 清空的数据库遗留的数据（选择）
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\ACCVALPrevious.xlsx'
        sheetName = 'ACC+VAL'
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
        df1 = df[['交易账号', '有效入金', '入金日期', '有效登录', '登录月份', '有效交易', '交易日期', '有效跟投', '跟投日期']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)

        # 转变某一列的类型
        df1['交易账号'] = df1['交易账号'].astype('str')

        df1['有效入金'] = df1['有效入金'].astype('str')
        df1['有效登录'] = df1['有效登录'].astype('str')
        df1['有效交易'] = df1['有效交易'].astype('str')
        df1['有效跟投'] = df1['有效跟投'].astype('str')

        df1['入金日期'] = df1['入金日期'].astype('str')
        df1['登录月份'] = df1['登录月份'].astype('str')
        df1['交易日期'] = df1['交易日期'].astype('str')
        df1['跟投日期'] = df1['跟投日期'].astype('str')

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


importAccValToSQLite()