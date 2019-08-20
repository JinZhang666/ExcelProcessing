#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importInertialTestersToSQLite():
    # SQLite中table的名字
    tableName = 'inertialtesters'

    # 建立数据库的连接
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO ' + tableName + '(mobile) ' \
                          'VALUES (?);'

        # 清空的数据库遗留的数据（选择）
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\证券、期权开户情况统计.xlsx'
        sheetName = '同事号码簿'
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
        df1 = df[['以下号码为研发同事，证券员工及测试机']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # 转变某一列的类型
        df1['以下号码为研发同事，证券员工及测试机'] = df1['以下号码为研发同事，证券员工及测试机'].astype('str')


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
        select_stmt = 'SELECT mobile FROM ' + tableName + ';'
        row = 0
        for mobile in db.execute(select_stmt).fetchall():
            print(str(mobile))
            row = row + 1
        print("row number: ", row)

#importInertialTestersToSQLite()

