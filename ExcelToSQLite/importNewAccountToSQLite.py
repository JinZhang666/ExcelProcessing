#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd


def importNewAccountToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src: 
            insert_template = "INSERT INTO newaccount " \
                    "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                    lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid, hrid, tjrsj, qdbm ) " \
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"


            #��յ����ݿ����������ݣ�ѡ��
            db.execute('DELETE FROM newaccount;')
            
            #����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET) 
            df = pd.read_excel('..\input\\newAcc.xlsx', sheetname = 'newAcc')
            #print("df Column headings:")
            #print(df.columns)
            
            #for sheet in src:
            #    if sheet.name == 'SQL Results':
            df1 = df[['KHH', 'KHRQ', 'KHJC', 'KHMC', 'SJ', 'YYB', '����Ӫҵ��', '��Ա���', '��Ա����', '��Ա���', '�ֻ�', 'Ӫҵ������',\
                    'Ӫҵ�����', 'HR���', 'TJRSJ', 'QDBM'    
                    ]] #ѡȡ����Ҫ������
            #print("df1 Column headings:")
            #print(df1.columns)
            #print(df1)
            
            # ת��operatetime�е�����
            # df1['OperateTime'] = df1['OperateTime'].astype('str')
                
            try: 
                print('Here is import new account to sqlite')
                db.executemany(insert_template, df1.values) #iter_rows() �Զ�������̧ͷ����
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback() 
            else:
                db.commit() 
                
            #����ǲ������е����ݶ���������
            """
            select_stmt = 'SELECT DISTINCT khcode FROM newaccount;'
            for row in db.execute(select_stmt).fetchall():
                #print("importing...", file_) 
                #print("event number:", row)
                print("inserted�������ױ��", row) 
            """
importNewAccountToSQLite() 
