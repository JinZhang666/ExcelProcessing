#!/usr/bin/python
# -*- coding: cp936 -*-

""" UpdateNewAccount.py
���� NewAccount �����ɾ��ĵĲ���
"""
import sqlite3
import datetime
#from SQLiteToExcel.getSheet2FromSQLite import *

class updateNewAccount:

    LastUpdateTime = None

    #reimport
    def reimport(df):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src:
            insert_template = "INSERT INTO newaccount " \
                              "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                              lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid, isLeftMarketPer ) " \
                              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

            # ��յ����ݿ����������ݣ�ѡ��
            db.execute('DELETE FROM newaccount;')
            df1 = df[['�����˺�', '����ʱ��', '�ͻ����', '�ͻ�����', '�����ֻ���', '���Ӫҵ������',\
                      '���Ӫҵ������', 'Ӫ����Ա����', 'Ӫ����Ա����', 'Ӫ����Ա���', 'Ӫ����Ա�ֻ���', 'Ӫ��Ӫҵ������', \
                      'Ӫ��Ӫҵ������', 'Ӫ����Ա���ǰԭֵ'
                      ]]  # ѡȡ����Ҫ������
            # print("df1 Column headings:")
            # print(df1.columns)
            # print(df1)

            # ת��operatetime�е�����
            # df1['OperateTime'] = df1['OperateTime'].astype('str')

            try:
                print('Here is import new account to sqlite based on sheet2')
                db.executemany(insert_template, df1.values)
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback()
            else:
                db.commit()

                # ����ǲ������е����ݶ���������
            """
            select_stmt = 'SELECT DISTINCT khcode FROM newaccount;'
            for row in db.execute(select_stmt).fetchall():
                #print("importing...", file_) 
                #print("event number:", row)
                print("inserted�������ױ��", row) 
            """
    '''
    sheet2��dataframe��Ϊ����������������newaccount
    '''
    def update(df):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            update_template = "UPDATE newaccount " \
                              "SET usrnameshort = ?," \
                              "usrname = ?," \
                              "khusrmobile = ?,"\
                              "lddepid = ?,"\
                              "lddepname = ?,"\
                              "marketperid = ?,"\
                              "marketpername = ?,"\
                              "marketpertype = ?,"\
                              "marketpermobile = ?,"\
                              "marketdepname = ?,"\
                              "marketdepid = ?"\
                              "WHERE khcode = ? AND khdate = ? "


            df1 = df[['�ͻ����', '�ͻ�����', '�����ֻ���', '���Ӫҵ������', \
                  '���Ӫҵ������', 'Ӫ����Ա����', 'Ӫ����Ա����', 'Ӫ����Ա���', \
                  'Ӫ����Ա�ֻ���', 'Ӫ��Ӫҵ������', 'Ӫ��Ӫҵ������', \
                  '�����˺�', '����ʱ��' \
                  ]]  # ѡȡ����Ҫ������
            print("df1 Column headings:")
            print(df1.columns)
            print(df1)

            try:
                print('3')
                db.executemany(update_template, df1.values)
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback()
            else:
                db.commit()
            updateNewAccount.LastUpdateTime = datetime.datetime.now()

#sheet2 = getSheet2FromSQLite()
#df = sheet2.getSheet2DataFrame()
# updateNewAccount.update(self.dataframe)
#updateNewAccount.update(df)

