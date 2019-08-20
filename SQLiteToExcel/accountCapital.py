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

            # ȡ�����е�account
            sqStatement = 'SELECT newaccount.khdate, newaccount.khcode, newaccount.usrnameshort, newaccount.usrname,\
                        newaccount.khusrmobile, newaccount.lddepid, newaccount.lddepname,\
                        newaccount.marketperid, newaccount.qdbm, newaccount.tjrsj, newaccount.marketdepid,\
                        newaccount.marketpername, newaccount.marketpertype, newaccount.marketpermobile, newaccount.marketdepname,\
                        newaccount.isLeftMarketPer\
                        FROM newaccount'

            # ̧ͷ����
            dst.write(0, 0, '����ʱ��')  # A
            dst.write(0, 1, '�����˺�')  # B
            dst.write(0, 2, '�ͻ����')  # C
            dst.write(0, 3, '�ͻ�����')  # D
            dst.write(0, 4, '�����ֻ���')  # E

            # ��ʱ����
            dst.write(0, 5, '7��31�պϼ��ʲ����')  # E

            dst.write(0, 6, '���Ӫҵ������')  # G
            dst.write(0, 7, '���Ӫҵ������')  # H
            dst.write(0, 8, 'Ӫ����Ա����')  # I
            dst.write(0, 9, 'Ӫ����Ա����')  # J
            dst.write(0, 10, 'Ӫ����Ա���')  # K
            dst.write(0, 11, 'Ӫ����Ա�ֻ���')  # L
            dst.write(0, 12, 'Ӫ��Ӫҵ������')  # M
            dst.write(0, 13, 'Ӫ��Ӫҵ������')  # N
            dst.write(0, 14, 'Ӫ����Ա���ǰԭֵ')  # O


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

                    # 7��31�պϼ��ʲ����
                    # ����khcode�ͻ��ţ��õ���7��31�պϼ��ʲ���7��31�յ����ʲ�������0���˻�������
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

                        # leavedMarketPeriOriginalId Ҫ������8λҪ������None
                        if isLeftMarketPer == 1 or isLeftMarketPer == 2:
                            # ˵�����Ӫ����Ա�Ѿ���ְ��
                            dst.write(row, 14, '��ְ')
                        else:
                            # None
                            dst.write(row, 14, '')

                    else:
                        if str(khcode).strip() == '395000010066':
                            dst.write(row, 8, "39708036")
                            dst.write(row, 9, "����")
                            dst.write(row, 10, "������")
                            dst.write(row, 11, "15659100118")
                            dst.write(row, 12, "3970")
                            dst.write(row, 13, "3970 ��ƽ���·֤ȯӪҵ��")

                        if str(khcode).strip() == '395000010065':
                            dst.write(row, 8, "31901042")
                            dst.write(row, 9, "�")
                            dst.write(row, 10, "�Ƹ�����ʦ")
                            dst.write(row, 11, "13072940875")
                            dst.write(row, 12, "3190")
                            dst.write(row, 13, "3190 �����ֹ�˾")

                        if str(khcode).strip() == '398000010900':
                            dst.write(row, 8, "37809097")
                            dst.write(row, 9, "�Ŷ��")
                            dst.write(row, 10, "�Ƹ�����ʦ")
                            dst.write(row, 11, "18247130746")
                            dst.write(row, 12, "3780")
                            dst.write(row, 13, "3780 ���ͺ�����ɽ��·֤ȯӪҵ��")

                    row = row + 1

            workbookdes.save('../output/effectiveATradeAccountCapital.xls')

# generate  excel
a = accountCapital()
a.generateAccountCapitalExcelFromSQLite()

