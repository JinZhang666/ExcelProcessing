#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd
from exceldoc import * 

def importMarketPerToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            #ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src: 
            insert_template = "INSERT INTO marketper " \
                    "(marketcode, markettype, marketname, marketmobile) " \
                    "VALUES (?, ?, ?, ?);"


            #��յ����ݿ�����������
            db.execute('DELETE FROM marketper;')

            #����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET) 
            df = pd.read_excel('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx', sheetname = 'SQL Results')
            print("df Column headings:")
            print(df.columns)
            #for sheet in src:
            #    if sheet.name == 'SQL Results':
            df1 = df[['��Ա���','��Ա���','��Ա����','�ֻ�']]
            print("df1 Column headings:") 
            print(df1.columns)
            print(df1)
            try: 
                print('3')
                db.executemany(insert_template, df1.values) #iter_rows() �Զ�������̧ͷ����
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback() 
            else:
                db.commit() 

            #����ǲ������е����ݶ���������
            select_stmt = 'SELECT DISTINCT marketcode FROM marketper;'
            for row in db.execute(select_stmt).fetchall():
                print('marketPerson: 1')
                print(';'.join(str(row)))

#importMarketPerToSQLite()
