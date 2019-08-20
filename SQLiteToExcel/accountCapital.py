#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3

from SQLiteQuery.capitalQuery import *
from SQLiteDataProcessing.userDayATradeUtility import *

'''
prerequisite: run getsheet2()
'''


class accountCapital:


    def generateAccountCapitalExcelFromSQLite(self):
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:

            workbookdes = xlwt.Workbook()
            dst = workbookdes.add_sheet('accoutCapital')
            cq = capitalQuery()
            #return: dictionary: {effectivekhcode: effectivetradedate}
            effectiveATradeUsersDict = userDayATradeUtility().geteffectiveATradeUsersAndDates()

            # 取出所有的account
            sqStatement = 'SELECT newaccount.khdate, newaccount.khcode, newaccount.usrnameshort, newaccount.usrname,\
                        newaccount.khusrmobile, newaccount.lddepid, newaccount.lddepname,\
                        newaccount.marketperid, newaccount.qdbm, newaccount.tjrsj, newaccount.marketdepid,\
                        newaccount.marketpername, newaccount.marketpertype, newaccount.marketpermobile, newaccount.marketdepname,\
                        newaccount.isLeftMarketPer\
                        FROM newaccount'

            # 抬头补充
            dst.write(0, 0, '开户时间')  # A
            dst.write(0, 1, '交易账号')  # B
            dst.write(0, 2, '客户简称')  # C
            dst.write(0, 3, '客户名称')  # D
            dst.write(0, 4, '开户手机号')  # E

            # 临时需求
            dst.write(0, 5, '7月31日合计资产余额')  # E

            dst.write(0, 6, '落地营业部代码')  # G
            dst.write(0, 7, '落地营业部名称')  # H
            dst.write(0, 8, '营销人员编码')  # I
            dst.write(0, 9, '营销人员名称')  # J
            dst.write(0, 10, '营销人员类别')  # K
            dst.write(0, 11, '营销人员手机号')  # L
            dst.write(0, 12, '营销营业部代码')  # M
            dst.write(0, 13, '营销营业部名称')  # N
            dst.write(0, 14, '营销人员变更前原值')  # O


            row = 1
            for khdate, khcode, usrnameshort, usrname, \
                khusrmobile, lddepid, lddepname, \
                marketperid, qdbm, tjrsj, marketdepid, \
                marketpername, marketpertype, marketpermobile, marketdepname , isLeftMarketPer\
                    in db.execute(sqStatement):

                if str(khcode).strip() in effectiveATradeUsersDict:
                #if '398000010171' in effectiveATradeUsersDict:
                    dst.write(row, 0, str(khdate))
                    dst.write(row, 1, str(khcode))
                    dst.write(row, 2, str(usrnameshort))
                    dst.write(row, 3, str(usrname))
                    dst.write(row, 4, str(khusrmobile))

                    # 7月31日合计资产余额
                    # 根据khcode客户号，得到他7月31日合计资产余额，7月31日当天资产余额大于0的人会有数据
                    # print(khcode)
                    zzc = cq.getZZCbyKHCodeAndDate(khcode, 20190731)
                    if zzc is not None:
                        #print(cq.getZZCbyKHCodeAndDate(khcode, 20190731)[0])
                        dst.write(row, 5, cq.getZZCbyKHCodeAndDate(khcode, 20190731)[0])
                    else:
                        dst.write(row, 5, '')

                    dst.write(row, 6, str(lddepid))
                    dst.write(row, 7, str(lddepname))

                    if str(khcode).strip() != '395000010066' and str(khcode).strip() != '395000010065' and str(
                            khcode).strip() != '398000010900':
                        dst.write(row, 8, str(marketperid))
                        dst.write(row, 9, str(marketpername))
                        dst.write(row, 10, str(marketpertype))
                        dst.write(row, 11, str(marketpermobile))
                        dst.write(row, 12, str(marketdepid))
                        dst.write(row, 13, str(marketdepid))

                        # leavedMarketPeriOriginalId 要不就是8位要不就是None
                        if isLeftMarketPer == 1 or isLeftMarketPer == 2:
                            # 说明这个营销人员已经离职了
                            dst.write(row, 14, '离职')
                        else:
                            # None
                            dst.write(row, 14, '')

                    else:
                        if str(khcode).strip() == '395000010066':
                            dst.write(row, 8, "39708036")
                            dst.write(row, 9, "陈凌")
                            dst.write(row, 10, "经纪人")
                            dst.write(row, 11, "15659100118")
                            dst.write(row, 12, "3970")
                            dst.write(row, 13, "3970 南平解放路证券营业部")

                        if str(khcode).strip() == '395000010065':
                            dst.write(row, 8, "31901042")
                            dst.write(row, 9, "李靖")
                            dst.write(row, 10, "财富管理师")
                            dst.write(row, 11, "13072940875")
                            dst.write(row, 12, "3190")
                            dst.write(row, 13, "3190 西安分公司")

                        if str(khcode).strip() == '398000010900':
                            dst.write(row, 8, "37809097")
                            dst.write(row, 9, "张多佳")
                            dst.write(row, 10, "财富管理师")
                            dst.write(row, 11, "18247130746")
                            dst.write(row, 12, "3780")
                            dst.write(row, 13, "3780 呼和浩特中山西路证券营业部")

                    row = row + 1

            workbookdes.save('../output/effectiveATradeAccountCapital.xls')

# generate  excel
a = accountCapital()
a.generateAccountCapitalExcelFromSQLite()

