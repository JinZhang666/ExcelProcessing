#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importATradeLogToSQLite():
    # SQLite��table������
    tableName = 'usrdayatrade'

    # �������ݿ������
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO ' + tableName + '(atradedate, khcode, atradenumber) ' \
                          'VALUES (?, ?, ?);'

        # ��յ����ݿ����������ݣ�ѡ��
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\\atrade.xlsx'
        sheetName = 'Sheet1'
        df = pd.read_excel(workbookPath, sheet_name=sheetName)

        """ 
        #��������һ�����ļ��е������ļ���ʱ��
        for root, dirs, files in os.walk(inputFolder):
            for file_ in files: 
                workbookPath = root + file_
                sheetName = os.path.splitext(file_)[0]
                df = pd.read_excel( workbookPath, sheetname = sheetName)
        """

        # ��ӡ���ű��̧ͷ
        print("df Column headings:")
        print(df.columns)

        # ��ӡժȡ��ĳ���У�ȷ���ֶ�˳����SQL�����ֶ�˳��һһ��Ӧ
        df1 = df[['����', '�ͻ���', '��Ͷ����']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)

        # ת��ĳһ�е�����
        df1['����'] = df1['����'].astype('str')
        df1['�ͻ���'] = df1['�ͻ���'].astype('str')
        df1['��Ͷ����'] = df1['��Ͷ����'].astype('str')

        try:
            print('3')
            db.executemany(insert_template, df1.values)
        except sqlite3.Error as e:
            print('2')
            print(e)
            db.rollback()
        else:
            db.commit()

        # ����ǲ������е����ݶ���������
        select_stmt = 'SELECT atradedate, khcode, atradenumber FROM ' + tableName + ';'
        row = 0
        for atradedate, khcode, atradenumber  in db.execute(select_stmt).fetchall():
            print(str(atradedate), str(khcode), str(atradenumber))
            row = row + 1
        print("row number: ", row)

importATradeLogToSQLite()
