#!/usr/bin/python
# -*- coding: cp936 -*-

""" UpdateLeftMarketPer.py
对于 leftmarketper 表格增删查改的操作
"""

import sqlite3

class updateLeftMarketPer:

    def update(leftpersonIds):
        # 把不存在于leftmarketper表格里的marketperson插入进去
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            insert_template = "INSERT OR REPLACE INTO leftmarketper " \
                              "(marketcode, markettype, marketname, marketmobile) " \
                              "VALUES (?, ?, ?, ?);"

            select_template = "SELECT marketcode, markettype, marketname, marketmobile FROM marketper" \
                              " WHERE marketcode = ?;"

            print('updating leftmarketper', leftpersonIds)
            for leftper in leftpersonIds:
                #print(len(leftper))
                for marketcode, markettype, marketname, marketmobile in db.execute(select_template, [leftper,]):
                    print(marketcode)
                    try:
                        print('3')
                        db.execute(insert_template, [marketcode, markettype, marketname, marketmobile])
                    except sqlite3.Error as e:
                        print('2')
                        print(e)
                        db.rollback()
                    else:
                        db.commit()

