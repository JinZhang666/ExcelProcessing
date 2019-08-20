#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importInertialTestersToSQLite():
    # SQLite��table������
    tableName = 'inertialtesters'

    # �������ݿ������
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        insert_template = 'INSERT INTO ' + tableName + '(mobile) ' \
                          'VALUES (?);'

        # ��յ����ݿ����������ݣ�ѡ��
        delete_template = 'DELETE FROM ' + tableName + ';'
        db.execute(delete_template)

        workbookPath = '..\input\֤ȯ����Ȩ�������ͳ��.xlsx'
        sheetName = 'ͬ�º��벾'
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
        df1 = df[['���º���Ϊ�з�ͬ�£�֤ȯԱ�������Ի�']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # ת��ĳһ�е�����
        df1['���º���Ϊ�з�ͬ�£�֤ȯԱ�������Ի�'] = df1['���º���Ϊ�з�ͬ�£�֤ȯԱ�������Ի�'].astype('str')


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
        select_stmt = 'SELECT mobile FROM ' + tableName + ';'
        row = 0
        for mobile in db.execute(select_stmt).fetchall():
            print(str(mobile))
            row = row + 1
        print("row number: ", row)

#importInertialTestersToSQLite()

