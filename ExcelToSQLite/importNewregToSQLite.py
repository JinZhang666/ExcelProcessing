#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd

def importNewregToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            #ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src: 
            insert_template_4 = "INSERT INTO newreg " \
                    "(usrmobile, marketcode, departmentid, createtime) " \
                    "VALUES (?, ?, ?, ?);"
            
            insert_template_9 = "INSERT INTO newreg "\
                    "(usrmobile, marketcode, departmentid, createtime, refid, refnickname, refrealname, refphone, pageindex) "\
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"

            #清空的数据库遗留的数据
            db.execute('DELETE FROM newreg;')

            #对于EXCEL文档里的每一个SHEET都导入数据库（simTrade中只有一个名为simTrade的SHEET) 
            df = pd.read_excel('..\input\\newReg.xlsx', sheetname = 'newReg')
            print("df Column headings:")
            print(df.columns)
            #for sheet in src:
            #    if sheet.name == 'SQL Results':
            
            #判断这个excel有几列
            df1 = None 
            if df.shape[1] == 4:
                df1 = df[['MOBILENO','MARKET_CODE','DEPARTMENT_ID','CREATETIME']]
            else:
                if df.shape[1] == 9 or df.shape[1] == 10:
                    print("There are " + "9" + " columns")
                    df1 = df[['MOBILENO', 'MARKET_CODE', 'DEPARTMENT_ID', 'CREATETIME', 'REFERRER_ID', 'NICK_NAME', 'REAL_NAME', 'PHONE', 'PAGE_INDEX']]
                    
            print("df1 Column headings:") 
            print(df1.columns)
            print(df1)
            
            try: 
                print('3')
                if df.shape[1] == 4:
                    db.executemany(insert_template_4, df1.values) #iter_rows() 自动跳过了抬头首行
                else:
                    if df.shape[1] == 9:
                        db.executemany(insert_template_9, df1.values)
                    else:
                        if df.shape[1] == 10:
                            db.executemany(insert_template_9, df1.values)

            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback() 
            else:
                db.commit() 

            #检查是不是所有的数据都被加载了
            select_stmt = 'SELECT DISTINCT usrmobile FROM newreg;'
            for row in db.execute(select_stmt).fetchall():
                print('newReg: 1')
                print(str(row))

importNewregToSQLite()
