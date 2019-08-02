#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importClientLoginDays05010513():

    # 建立数据库的连接
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src:
        insert_template = "INSERT INTO clientlogindays05010513" \
                          "(PHONE, COUNT) " \
                          "VALUES (?, ?);"

        # 清空的数据库遗留的数据（选择）
        db.execute('DELETE FROM clientlogindays05010513;')

        workbookPath = '..\hisinput\\tradelogin\星途-奇点股票20190501-20190513登录天数统计.xlsx'
        df = pd.read_excel(workbookPath, sheet_name='星途-奇点股票20190501-20190513登录天数统计')

        # 打印整张表的抬头
        print("df Column headings:")
        print(df.columns)

        # 打印摘取的某几列，确保字段顺序与SQL语句的字段顺序一一对应
        df1 = df[['PHONE', 'COUNT(DISTINCTTT.DDD)']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # 转变某一列的类型
        df1['PHONE'] = df1['PHONE'].astype('str')
        df1['COUNT(DISTINCTTT.DDD)'] = df1['COUNT(DISTINCTTT.DDD)'].astype('str')

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
        select_stmt = 'SELECT * FROM clientlogindays05010513;'
        row = 0
        for phone, count in db.execute(select_stmt).fetchall():
            print(str(phone), str(count))
            row = row + 1
        print("row number: ", row)

importClientLoginDays05010513()
