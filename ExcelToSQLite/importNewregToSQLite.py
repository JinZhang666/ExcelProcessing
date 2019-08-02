#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd

def importNewregToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            #ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src: 
            insert_template_4 = "INSERT INTO newreg " \
                    "(usrmobile, marketcode, departmentid, createtime) " \
                    "VALUES (?, ?, ?, ?);"
            
            insert_template_9 = "INSERT INTO newreg "\
                    "(usrmobile, marketcode, departmentid, createtime, refid, refnickname, refrealname, refphone, pageindex) "\
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"

            #��յ����ݿ�����������
            db.execute('DELETE FROM newreg;')

            #����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET) 
            df = pd.read_excel('..\input\\newReg.xlsx', sheetname = 'newReg')
            print("df Column headings:")
            print(df.columns)
            #for sheet in src:
            #    if sheet.name == 'SQL Results':
            
            #�ж����excel�м���
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
                    db.executemany(insert_template_4, df1.values) #iter_rows() �Զ�������̧ͷ����
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

            #����ǲ������е����ݶ���������
            select_stmt = 'SELECT DISTINCT usrmobile FROM newreg;'
            for row in db.execute(select_stmt).fetchall():
                print('newReg: 1')
                print(str(row))

importNewregToSQLite()
