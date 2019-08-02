#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import pandas as pd

#By Sheet6
def importAccountToSQLite():
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src:
        insert_template = "INSERT INTO account " \
                          "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid ) " \
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

        # ��յ����ݿ����������ݣ�ѡ��
        db.execute('DELETE FROM account;')

        # ����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET)
        df = pd.read_excel('..\input\datatoolsheet6.xlsx', sheetname='Sheet1')
        #print("df Column headings:")
        #print(df.columns)

        # for sheet in src:
        #    if sheet.name == 'SQL Results':
        df1 = df[[ '�����˺�', '����ʱ��', '�ͻ����', '�ͻ�����', '�����ֻ���', '���Ӫҵ������',\
                   '���Ӫҵ������', 'Ӫ����Ա����', 'Ӫ����Ա����', 'Ӫ����Ա���', 'Ӫ����Ա�ֻ���', 'Ӫ��Ӫҵ������', 'Ӫ��Ӫҵ������'
                  ]]  # ѡȡ����Ҫ������
        #print("df1 Column headings:")
        #print(df1.columns)
        #print(df1)

        # ת��operatetime�е�����
        # df1['OperateTime'] = df1['OperateTime'].astype('str')

        try:
            print('Here is import account to sqlite')
            db.executemany(insert_template, df1.values)  # iter_rows() �Զ�������̧ͷ����
        except sqlite3.Error as e:
            #print('2')
            #print(e)
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

# By ACC + VAL
def importAccountToSQLiteFromACCVAL():
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        # ExcelDocument('..\input\Ӫ����Ա��Ӫҵ���б�.xlsx') as src:
        insert_template = "INSERT INTO account " \
                          "(khcode, khdate, usrnameshort, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid ) " \
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

        # ��յ����ݿ����������ݣ�ѡ��
        db.execute('DELETE FROM account;')

        # ����EXCEL�ĵ����ÿһ��SHEET���������ݿ⣨simTrade��ֻ��һ����ΪsimTrade��SHEET)
        df = pd.read_excel('..\input\ACCVALPrevious.xlsx', sheetname='ACC+VAL')
        #print("df Column headings:")
        #print(df.columns)

        # for sheet in src:
        #    if sheet.name == 'SQL Results':
        df1 = df[[ '�����˺�', '����ʱ��', '�ͻ����', '�����ֻ���', '��ز�����',\
                   '��ز�����', 'Ӫ���˱���', 'Ӫ��������', 'Ӫ�������', 'Ӫ�����ֻ�',\
                   'Ӫ��������', 'Ӫ��������']]  # ѡȡ����Ҫ������
        #print("df1 Column headings:")
        #print(df1.columns)
        #print(df1)

        # ת��operatetime�е�����
        # df1['OperateTime'] = df1['OperateTime'].astype('str')

        try:
            print('Here is import account to sqlite')
            db.executemany(insert_template, df1.values)  # iter_rows() �Զ�������̧ͷ����
        except sqlite3.Error as e:
            #print('2')
            print(e)
            db.rollback()
        else:
            db.commit()

            # ����ǲ������е����ݶ���������

#importAccountToSQLiteFromACCVAL()
#importAccountToSQLite()
