#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3 
from exceldoc import * 

def importMarketDepToSQLite():
    """excel"""
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db, \
            ExcelDocument('..\input\营销人员和营业部列表.xlsx') as src: 
            insert_template = "INSERT INTO marketdep " \
                    "(depid, depname) " \
                    "VALUES (?, ?);"

            #清空的数据库遗留的数据
            db.execute('DELETE FROM marketdep;')

            #对于EXCEL文档里的每一个SHEET都导入数据库（simTrade中只有一个名为simTrade的SHEET) 
            for sheet in src:
                if sheet.name == 'branchlist':
                    try: 
                        print('3')
                        db.executemany(insert_template, sheet.iter_rows()) #iter_rows() 自动跳过了抬头首行
                    except sqlite3.Error as e:
                        print('2')
                        print(e)
                        db.rollback() 
                    else:
                        db.commit() 

            #检查是不是所有的数据都被加载了
            select_stmt = 'SELECT DISTINCT depid FROM marketdep;'
            for row in db.execute(select_stmt).fetchall():
                print('1')
                print(';'.join(str(row)))

#importMarketDepToSQLite()
