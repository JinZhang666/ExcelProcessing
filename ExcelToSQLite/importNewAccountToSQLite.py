#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd


def importNewAccountToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            # ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src: 
            insert_template = "INSERT INTO newaccount " \
                    "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                    lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid, hrid, tjrsj, qdbm ) " \
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"


            #清空的数据库遗留的数据（选择）
            db.execute('DELETE FROM newaccount;')
            
            #对于EXCEL文档里的每一个SHEET都导入数据库（simTrade中只有一个名为simTrade的SHEET) 
            df = pd.read_excel('..\input\\newAcc.xlsx', sheetname = 'newAcc')
            #print("df Column headings:")
            #print(df.columns)
            
            #for sheet in src:
            #    if sheet.name == 'SQL Results':
            df1 = df[['KHH', 'KHRQ', 'KHJC', 'KHMC', 'SJ', 'YYB', '开户营业部', '人员编号', '人员姓名', '人员类别', '手机', '营业部名称',\
                    '营业部编号', 'HR编号', 'TJRSJ', 'QDBM'    
                    ]] #选取你需要的列数
            #print("df1 Column headings:")
            #print(df1.columns)
            #print(df1)
            
            # 转变operatetime列的类型
            # df1['OperateTime'] = df1['OperateTime'].astype('str')
                
            try: 
                print('Here is import new account to sqlite')
                db.executemany(insert_template, df1.values) #iter_rows() 自动跳过了抬头首行
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback() 
            else:
                db.commit() 
                
            #检查是不是所有的数据都被加载了
            """
            select_stmt = 'SELECT DISTINCT khcode FROM newaccount;'
            for row in db.execute(select_stmt).fetchall():
                #print("importing...", file_) 
                #print("event number:", row)
                print("inserted开户交易编号", row) 
            """
importNewAccountToSQLite() 
