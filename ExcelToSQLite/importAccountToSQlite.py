#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd

#By Sheet6
def importAccountToSQLite():
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src:
        insert_template = "INSERT INTO account " \
                          "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid ) " \
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

        # 清空的数据库遗留的数据（选择）
        db.execute('DELETE FROM account;')

        # 对于EXCEL文档里的每一个SHEET都导入数据库（simTrade中只有一个名为simTrade的SHEET)
        df = pd.read_excel('..\input\datatoolsheet6.xlsx', sheetname='Sheet1')
        #print("df Column headings:")
        #print(df.columns)

        # for sheet in src:
        #    if sheet.name == 'SQL Results':
        df1 = df[[ '交易账号', '开户时间', '客户简称', '客户名称', '开户手机号', '落地营业部代码',\
                   '落地营业部名称', '营销人员编码', '营销人员名称', '营销人员类别', '营销人员手机号', '营销营业部名称', '营销营业部代码'
                  ]]  # 选取你需要的列数
        #print("df1 Column headings:")
        #print(df1.columns)
        #print(df1)

        # 转变operatetime列的类型
        # df1['OperateTime'] = df1['OperateTime'].astype('str')

        try:
            print('Here is import account to sqlite')
            db.executemany(insert_template, df1.values)  # iter_rows() 自动跳过了抬头首行
        except sqlite3.Error as e:
            #print('2')
            #print(e)
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

# By ACC + VAL
def importAccountToSQLiteFromACCVAL():
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src:
        insert_template = "INSERT INTO account " \
                          "(khcode, khdate, usrnameshort, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid ) " \
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

        # 清空的数据库遗留的数据（选择）
        db.execute('DELETE FROM account;')

        # 对于EXCEL文档里的每一个SHEET都导入数据库（simTrade中只有一个名为simTrade的SHEET)
        df = pd.read_excel('..\input\ACCVALPrevious.xlsx', sheetname='ACC+VAL')
        #print("df Column headings:")
        #print(df.columns)

        # for sheet in src:
        #    if sheet.name == 'SQL Results':
        df1 = df[[ '交易账号', '开户时间', '客户简称', '开户手机号', '落地部代码',\
                   '落地部名称', '营销人编码', '营销人名称', '营销人类别', '营销人手机',\
                   '营销部名称', '营销部代码']]  # 选取你需要的列数
        #print("df1 Column headings:")
        #print(df1.columns)
        #print(df1)

        # 转变operatetime列的类型
        # df1['OperateTime'] = df1['OperateTime'].astype('str')

        try:
            print('Here is import account to sqlite')
            db.executemany(insert_template, df1.values)  # iter_rows() 自动跳过了抬头首行
        except sqlite3.Error as e:
            #print('2')
            print(e)
            db.rollback()
        else:
            db.commit()

            # 检查是不是所有的数据都被加载了

#importAccountToSQLiteFromACCVAL()
#importAccountToSQLite()
