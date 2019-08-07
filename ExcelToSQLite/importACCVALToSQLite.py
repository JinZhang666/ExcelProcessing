#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os

def importAccValToSQLite():
    # SQLite��table������
    tableName = 'accval'

    # �������ݿ������
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO ' + tableName + '(khcode, iseffectivecapital, capitaldate, ' \
                                                       'iseffectivelogin, logindate, ' \
                                                       'iseffectivetrade, tradedate, ' \
                                                       'iseffectiveatrade, atradedate)' \
                          'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'

        # ��յ����ݿ����������ݣ�ѡ��
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\ACCVALPrevious.xlsx'
        sheetName = 'ACC+VAL'
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
        df1 = df[['�����˺�', '��Ч���', '�������', '��Ч��¼', '��¼�·�', '��Ч����', '��������', '��Ч��Ͷ', '��Ͷ����']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)

        # ת��ĳһ�е�����
        df1['�����˺�'] = df1['�����˺�'].astype('str')

        df1['��Ч���'] = df1['��Ч���'].astype('str')
        df1['��Ч��¼'] = df1['��Ч��¼'].astype('str')
        df1['��Ч����'] = df1['��Ч����'].astype('str')
        df1['��Ч��Ͷ'] = df1['��Ч��Ͷ'].astype('str')

        df1['�������'] = df1['�������'].astype('str')
        df1['��¼�·�'] = df1['��¼�·�'].astype('str')
        df1['��������'] = df1['��������'].astype('str')
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
        select_stmt = 'SELECT khcode FROM ' + tableName + ';'
        row = 0
        for khcode in db.execute(select_stmt).fetchall():
            print(str(khcode))
            row = row + 1
        print("row number: ", row)


importAccValToSQLite()