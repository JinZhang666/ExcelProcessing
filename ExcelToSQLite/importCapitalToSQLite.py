#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importCapitalToSQLite():

    # �������ݿ������
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src:
        insert_template = "INSERT INTO usrDayInCapital" \
                          "(date, khcode, zzc) " \
                          "VALUES (?, ?, ?);"

        # ��յ����ݿ����������ݣ�ѡ��
        db.execute('DELETE FROM usrDayInCapital;')

        workbookPath = '..\input\capital\capital.xlsx'
        df = pd.read_excel(workbookPath, sheet_name='SQL Results')

        # ��ӡ���ű��̧ͷ
        print("df Column headings:")
        print(df.columns)

        # ��ӡժȡ��ĳ���У�ȷ���ֶ�˳����SQL�����ֶ�˳��һһ��Ӧ
        df1 = df[['RQ', 'KHH', 'ZZC']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # ת��ĳһ�е�����
        df1['RQ'] = df1['RQ'].astype('str')
        df1['KHH'] = df1['KHH'].astype('str')

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
        select_stmt = 'SELECT * FROM usrDayInCapital;'
        row = 0
        for rq, khh, zzc in db.execute(select_stmt).fetchall():
            print(str(rq), str(khh), str(zzc))
            row = row + 1
        print("row number: ", row)

#importCapitalToSQLite()
