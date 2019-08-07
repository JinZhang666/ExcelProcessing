#!/usr/bin/python
# -*- coding: cp936 -*-

import os
import sqlite3
import re
import pandas as pd


def importHisClientLoginEventToSQLite():
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src:
        insert_template1 = "INSERT INTO hisclientloginevent " \
                          "(clientid, logindate, logintime, eventtype, eventmsg) " \
                          "VALUES (?, ?, ?, ?, ?);"
        insert_template2 = "INSERT INTO hisclientloginevent " \
                           "(clientid, logindate, eventmsg) " \
                           "VALUES (?, ?, ?);"
        # ��յ����ݿ����������ݣ�ѡ��
        db.execute('DELETE FROM hisclientloginevent;')

        totalNumberOfRecords = 0
        totalNumberOfFiles = 0

        inputFolder = '..\hisInput\\tradelogin\\'
        for root, dirs, files in os.walk(inputFolder):
            for file_ in files:
                workbookName = os.path.splitext(file_)[0]
                sheetName = str(os.path.splitext(file_)[0])

                if re.match(r'2019.', file_) is not None:
                    print(file_)
                    df = pd.read_excel(root + file_, sheet_name=sheetName)
                    #print("df Column headings:")
                    #print(df.columns)

                    no = df.iloc[:, 0].size
                    print(no) # ���� 3
                    totalNumberOfRecords = totalNumberOfRecords + no

                    # for sheet in src:
                    #    if sheet.name == 'SQL Results':
                    df1 = None
                    if df.shape[1] == 7:
                        df1 = df[['OperatorID', 'OperateDate', 'OperateTime', 'EventType', 'EventMsg']]  # ѡȡ����Ҫ������
                        # ת��operatetime�е�����
                        df1['OperateDate'] = df1['OperateDate'].astype('str')
                        df1['OperateTime'] = df1['OperateTime'].astype('str')
                        df1['EventType'] = df1['EventType'].astype('str')
                        df1['EventMsg'] = df1['EventMsg'].astype('str')
                    else:
                        if df.shape[1] == 5:
                            df1 = df[['OperatorID', 'OperateDate', 'EventMsg']]  # ѡȡ����Ҫ������

                    try:
                        #print('3')
                        if df.shape[1] == 7:
                            print('7')
                            db.executemany(insert_template1, df1.values)  # iter_rows() �Զ�������̧ͷ����
                        else:
                            if df.shape[1] == 5:
                                print('5')
                                db.executemany(insert_template2, df1.values)  # iter_rows() �Զ�������̧ͷ����
                        totalNumberOfFiles = totalNumberOfFiles + 1
                    except sqlite3.Error as e:
                        print('2')
                        print(e)
                        db.rollback()
                    else:
                        db.commit()

        print('total records', totalNumberOfRecords)
        print('total files', totalNumberOfFiles)

        # ����ǲ������е����ݶ���������
        #select_stmt = 'SELECT DISTINCT eventno FROM clientloginevent;'
        #for row in db.execute(select_stmt).fetchall():
            #print("importing...", file_)
            #print("event number:", row)


importHisClientLoginEventToSQLite()
