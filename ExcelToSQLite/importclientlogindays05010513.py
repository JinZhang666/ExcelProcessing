#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd
import os


def importClientLoginDays05010513():

    # �������ݿ������
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src:
        insert_template = "INSERT INTO clientlogindays05010513" \
                          "(PHONE, COUNT) " \
                          "VALUES (?, ?);"

        # ��յ����ݿ����������ݣ�ѡ��
        db.execute('DELETE FROM clientlogindays05010513;')

        workbookPath = '..\hisinput\\tradelogin\��;-����Ʊ20190501-20190513��¼����ͳ��.xlsx'
        df = pd.read_excel(workbookPath, sheet_name='��;-����Ʊ20190501-20190513��¼����ͳ��')

        # ��ӡ���ű��̧ͷ
        print("df Column headings:")
        print(df.columns)

        # ��ӡժȡ��ĳ���У�ȷ���ֶ�˳����SQL�����ֶ�˳��һһ��Ӧ
        df1 = df[['PHONE', 'COUNT(DISTINCTTT.DDD)']]
        print("df1 Column headings:")
        print(df1.columns)
        print(df1)


        # ת��ĳһ�е�����
        df1['PHONE'] = df1['PHONE'].astype('str')
        df1['COUNT(DISTINCTTT.DDD)'] = df1['COUNT(DISTINCTTT.DDD)'].astype('str')

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
        select_stmt = 'SELECT * FROM clientlogindays05010513;'
        row = 0
        for phone, count in db.execute(select_stmt).fetchall():
            print(str(phone), str(count))
            row = row + 1
        print("row number: ", row)

importClientLoginDays05010513()
