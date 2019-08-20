#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
from exceldoc import * 

def importMarketDepToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db, \
            ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src: 
            insert_template = "INSERT INTO marketdep " \
                    "(depid, depname) " \
                    "VALUES (?, ?);"

            #��յ����ݿ�����������
            db.execute('DELETE FROM marketdep;')

            #����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET) 
            for sheet in src:
                if sheet.name == 'branchlist':
                    try: 
                        print('3')
                        db.executemany(insert_template, sheet.iter_rows()) #iter_rows() �Զ�������̧ͷ����
                    except sqlite3.Error as e:
                        print('2')
                        print(e)
                        db.rollback() 
                    else:
                        db.commit() 

            #����ǲ������е����ݶ���������
            select_stmt = 'SELECT DISTINCT depid FROM marketdep;'
            for row in db.execute(select_stmt).fetchall():
                print('1')
                print(';'.join(str(row)))

#importMarketDepToSQLite()
