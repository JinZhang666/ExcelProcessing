#!/usr/bin/python
# -*- coding: cp936 -*-

""" UpdateNewAccount.py
对于 NewAccount 表格增删查改的操作
"""
import sqlite3
import datetime
#from SQLiteToExcel.getSheet2FromSQLite import *

class updateNewAccount:

    LastUpdateTime = None

    #reimport
    def reimport(df):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            # ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src:
            insert_template = "INSERT INTO newaccount " \
                              "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                              lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid, isLeftMarketPer ) " \
                              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

            # 清空的数据库遗留的数据（选择）
            db.execute('DELETE FROM newaccount;')
            df1 = df[['交易账号', '开户时间', '客户简称', '客户名称', '开户手机号', '落地营业部代码',\
                      '落地营业部名称', '营销人员编码', '营销人员名称', '营销人员类别', '营销人员手机号', '营销营业部名称', \
                      '营销营业部代码', '营销人员变更前原值'
                      ]]  # 选取你需要的列数
            # print("df1 Column headings:")
            # print(df1.columns)
            # print(df1)

            # 转变operatetime列的类型
            # df1['OperateTime'] = df1['OperateTime'].astype('str')

            try:
                print('Here is import new account to sqlite based on sheet2')
                db.executemany(insert_template, df1.values)
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback()
            else:
                db.commit()

                # 检查是不是所有的数据都被加载了
            """
            select_stmt = 'SELECT DISTINCT khcode FROM newaccount;'
            for row in db.execute(select_stmt).fetchall():
                #print("importing...", file_) 
                #print("event number:", row)
                print("inserted开户交易编号", row) 
            """
    '''
    sheet2的dataframe作为参数传过来，更新newaccount
    '''
    def update(df):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            update_template = "UPDATE newaccount " \
                              "SET usrnameshort = ?," \
                              "usrname = ?," \
                              "khusrmobile = ?,"\
                              "lddepid = ?,"\
                              "lddepname = ?,"\
                              "marketperid = ?,"\
                              "marketpername = ?,"\
                              "marketpertype = ?,"\
                              "marketpermobile = ?,"\
                              "marketdepname = ?,"\
                              "marketdepid = ?"\
                              "WHERE khcode = ? AND khdate = ? "


            df1 = df[['客户简称', '客户名称', '开户手机号', '落地营业部代码', \
                  '落地营业部名称', '营销人员编码', '营销人员名称', '营销人员类别', \
                  '营销人员手机号', '营销营业部名称', '营销营业部代码', \
                  '交易账号', '开户时间' \
                  ]]  # 选取你需要的列数
            print("df1 Column headings:")
            print(df1.columns)
            print(df1)

            try:
                print('3')
                db.executemany(update_template, df1.values)
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback()
            else:
                db.commit()
            updateNewAccount.LastUpdateTime = datetime.datetime.now()

#sheet2 = getSheet2FromSQLite()
#df = sheet2.getSheet2DataFrame()
# updateNewAccount.update(self.dataframe)
#updateNewAccount.update(df)

