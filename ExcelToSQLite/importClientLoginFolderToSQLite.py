#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd
import os 
from exceldoc import * 

def importClientLoginFolderToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src: 
            insert_template1 = "INSERT INTO clientloginevent " \
                    "(clientid, logindate, logintime, eventtype, eventmsg) " \
                    "VALUES (?, ?, ?, ?, ?);"
            insert_template2 = "INSERT INTO clientloginevent " \
                    "(clientid, logindate, eventmsg) " \
                    "VALUES (?, ?, ?);"


            #��յ����ݿ����������ݣ�ѡ��
            print('delete')
            db.execute('DELETE FROM clientloginevent;')
      
            inputFolder = '..\input\clientLogin\\'
            for root, dirs, files in os.walk(inputFolder):
                for file_ in files:
                    #����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET) 
                    sheetName = os.path.splitext(file_)[0]
                    df = pd.read_excel( root + file_, sheetname = sheetName)
                    print("df Column headings:")
                    print(df.columns)


                    df1 = None
                    if df.shape[1] == 7:
                        df1 = df[['OperatorID','OperateDate','OperateTime','EventType', 'EventMsg']] #ѡȡ����Ҫ������
                        # ת��operatetime�е�����
                        df1['OperateTime'] = df1['OperateTime'].astype('str')
                    else:
                        if df.shape[1] == 5:
                            df1 = df[['OperatorID','OperateDate', 'EventMsg']] #ѡȡ����Ҫ������

                    print("df1 Column headings:")
                    print(df1.columns)
                    print(df1)


                    try:
                        if df.shape[1] == 7:
                            print('7')
                            db.executemany(insert_template1, df1.values) #iter_rows() �Զ�������̧ͷ����
                        else:
                            if df.shape[1] == 5:
                                print('5')
                                db.executemany(insert_template2, df1.values)  # iter_rows() �Զ�������̧ͷ����

                    except sqlite3.Error as e:
                        print('2')
                        print(e)
                        db.rollback() 
                    else:
                        db.commit() 

                    #����ǲ������е����ݶ���������
                    select_stmt = 'SELECT DISTINCT eventno FROM clientloginevent;'
                    for row in db.execute(select_stmt).fetchall():
                        print("importing...", file_) 
                        print("event number:", row)

importClientLoginFolderToSQLite()
