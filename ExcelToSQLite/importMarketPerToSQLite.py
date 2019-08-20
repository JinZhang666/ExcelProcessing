#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
import pandas as pd
from exceldoc import * 

def importMarketPerToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            #ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src: 
            insert_template = "INSERT INTO marketper " \
                    "(marketcode, markettype, marketname, marketmobile) " \
                    "VALUES (?, ?, ?, ?);"


            #清空的数据库遗留的数据
            db.execute('DELETE FROM marketper;')

            #对于EXCEL文档里的每一个SHEET都导入数据库（simTrade中只有一个名为simTrade的SHEET) 
            df = pd.read_excel('..\input\营销人员和营业部列表.xlsx', sheetname = 'SQL Results')
            print("df Column headings:")
            print(df.columns)
            #for sheet in src:
            #    if sheet.name == 'SQL Results':
            df1 = df[['人员编号','人员类别','人员姓名','手机']]
            print("df1 Column headings:") 
            print(df1.columns)
            print(df1)
            try: 
                print('3')
                db.executemany(insert_template, df1.values) #iter_rows() 自动跳过了抬头首行
            except sqlite3.Error as e:
                print('2')
                print(e)
                db.rollback() 
            else:
                db.commit() 

            #检查是不是所有的数据都被加载了
            select_stmt = 'SELECT DISTINCT marketcode FROM marketper;'
            for row in db.execute(select_stmt).fetchall():
                print('marketPerson: 1')
                print(';'.join(str(row)))

#importMarketPerToSQLite()
