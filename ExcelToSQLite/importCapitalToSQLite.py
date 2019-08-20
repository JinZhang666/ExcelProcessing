#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importCapitalToSQLite():

    # 建立数据库的连接
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src:
        insert_template = "INSERT INTO usrDayInCapital" \
                          "(date, khcode, zzc) " \
                          "VALUES (?, ?, ?);"

        # 清空的数据库遗留的数据（选择）
        db.execute('DELETE FROM usrDayInCapital;')

        workbookPath = '..\input\capital\capital.xlsx'
        df = pd.read_excel(workbookPath, sheet_name='SQL Results')

        # 打印整张表的抬头
        print("df Column headings:")
        print(df.columns)

        # 打印摘取的某几列，确保字段顺序与SQL语句的字段顺序一一对应
        df1 = df[['RQ', 'KHH', 'ZZC']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # 转变某一列的类型
        df1['RQ'] = df1['RQ'].astype('str')
        df1['KHH'] = df1['KHH'].astype('str')

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
        select_stmt = 'SELECT * FROM usrDayInCapital;'
        row = 0
        for rq, khh, zzc in db.execute(select_stmt).fetchall():
            print(str(rq), str(khh), str(zzc))
            row = row + 1
        print("row number: ", row)

#importCapitalToSQLite()
