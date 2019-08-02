#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
""" UpdateLeftAccount.py
对于 leftaccount 表格增删查改的操作
"""

class updateLeftAccount:

    def update(leftAccounts):
        # 插入leftaccount, 存在的就replace
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            insert_template = "INSERT OR REPLACE INTO leftaccount " \
                          "(khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid ) " \
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"


            select_template = "SELECT  khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid FROM  account WHERE khcode = ?;"

            print('update', leftAccounts)
            for leftaccount in leftAccounts:
                # print(len(leftper))
                rows = db.execute(select_template, [str(leftaccount).strip(), ])
                # consume sql result to avoid ERROR: Cursor needed to be reset because of commit/rollback and can no longer be fetched from
                rows = list(rows)
                for khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                        lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid in rows:
                    try:
                        print('Here is inserting leftacoount')
                        db.execute(insert_template, [khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                        lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid])
                    except sqlite3.Error as e:
                        print('2')
                        print(e)
                        db.rollback()
                    else:
                        db.commit()

#updateLeftAccount.update([316000032159, 326000020573, 326000020589, 323000031986, 378000011703])