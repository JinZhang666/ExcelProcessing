#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd


def importAccountValueToSQLite():
    # SQLite中table的名字
    tableName = 'accountvalue'

    # 建立数据库的连接
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO accountvalue (khcode, value) ' \
                          'VALUES (?, ?);'

        # 清空的数据库遗留的数据（选择）
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\\newAcc+val+wechat.xlsx'
        sheetName = 'Sheet1'
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
        df1 = df[['交易账号', '价值']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # 转变某一列的类型
        df1['交易账号'] = df1['交易账号'].astype('str')
        df1['价值'] = df1['价值'].astype('str')


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
        select_stmt = 'SELECT *  FROM ' + tableName + ';'
        row = 0
        for khcode, value in db.execute(select_stmt).fetchall():
            print(str(khcode), str(value))
            row = row + 1
        print("row number: ", row)

#importAccountValueToSQLite()
