#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3  
import csv 
import xlrd  
import xlwt
import pandas as pd
from SQLiteDataProcessing.clientLoginEventUtility import *
from ExcelToSQLite.importNewAccountToSQLite import *
from UpdateSQliteTables.updateNewAccount import *
from UpdateSQliteTables.updateLeftMarketPer import *

'''
1. import newacc 
2. �õ�sheet2 
3. ����sheet2ȥupdate newacc 
'''
class getSheet2FromSQLite:

    def __init__(self):
        self.dataframe = None
        self.leftMarketPerIds = []
        self.internetReferUsers = []

    def generateSheet2ExcelFromSQLite(self):

        # import clean newacc to SQLite
        print('Preparing to import clean newaccount')
        importNewAccountToSQLite()
        print('Finsh import clean newaccount')

        # checkMarketRelation �������Ӫ����Ա����ǲ�����д�����û����д�������·����ҡ���ְ��Ա��Ӫ����ϵ����
        # 1. �鿴QDBM�ֶ�
        # 1��������ֶ�����'_'��������ʽ����ô�������ĵ�3���ַ���, �����ǿ��ַ���/4λӪ������/8λӪ�����룬�����һ��8λ��Ӫ����Ա���룬��˵������Ա��Ϊ��ְ��û����д��Ӫ����Ա����ֱ��дӪ��������;
        # * marketperid = ���ֶ�ǰ4λ����
        # * marketdepid = ���ֶ�ǰ4λ����
        # * marketdepname = Ӫ��Ӫҵ�������Ӧ��Ӫ�������ƣ���input/��Ӫ����Ա��Ӫҵ���б�excel��branchlist���в��ҵ���Ӧ��֧������ //��db��marketdep���в��ң�
        # 2�����QDBM�ֶ����Ҳ������8λ��Ӫ������
        #       2.�鿴newacc�����TJRSJ�ֶ�
        #       1��������ֶ���8λ���룬��ô˵�����Ա���Ѿ���ְ��Ӫ����Ա����ֱ��ддӪҵ�����룺
        #       * marketperid = ���ֶε�ǰ4λ����
        #       * marketdepid = ���ֶε�ǰ4λ����
        #       * marketdepname = Ӫ��Ӫҵ�������Ӧ��Ӫ�������ƣ���input/��Ӫ����Ա��Ӫҵ���б�excel��branchlist���в��ҵ���Ӧ��֧������ //��db��marketdep���в��ң�
        #       2���������8λ���룬ʲô��������marketperid, marketdepid, marketdepname ������
    
        class CheckMarketRelation:
            """ ���ڲ���Ӫ����ϵ """
            """ return: 1. Ӫ����Ա����(marketperid) 2. Ӫ��Ӫҵ������(marketdepid)"""
        
            def check(marketperid, qdbm, tjrsj, marketdepid):
            
                #print('Here is checkMarketrelation')
                mpi = marketperid
                mdi = marketdepid
                mpiOriginal = None
                #print('checkMarketRelation 1')
           
                if marketperid is None:
                    #print('marketperid is none')
                
                    try:
                        #��QDBM
                        """
                        print(qdbm)
                        print(len(str(qdbm).split('_')))
                        print(str(qdbm).split('_')) 
                        print(len(str(qdbm).split('_')[2]))
                        print(tjrsj) 
                        print( len(str(tjrsj)) )
                        """
                        if not (qdbm is None) and len(str(qdbm).split('_')) >=3:
                            #print('check 1')
                            mpi = str(qdbm).split('_')[2] #��'_'�����ĵ�3���ַ�������mpi,������4λ����Ҳ����λ�գ�Ҳ������8λ
                            if len(str(qdbm).split('_')[2]) == 8:

                                #register leftperid
                                self.leftMarketPerIds.append(str(qdbm).split('_')[2])

                                mpi = str(qdbm).split('_')[2][0:4]
                                mpiOriginal = str(qdbm).split('_')[2]
                            mdi = mpi
                
                        else:
                            #��TJRSJ
                            if not(tjrsj is None) and len(str(tjrsj).strip()) == 8:
                                #print('check 2')
                                # register leftperid
                                self.leftMarketPerIds.append(str(tjrsj).strip())

                                mpi = str(tjrsj)[0:4]
                                mdi = mpi
                                mpiOriginal = str(tjrsj)
                    except Exception:
                        print('exception in check Marketrelation')
                

                #print(mpi)
                #print(mdi)

                #mpiOriginalһ����8λ��
                return str(mpi), str(mdi), str(mpiOriginal)


        # �����ݿ������Լ���Ҫʹ�õı���ĵ�
        # open('sheet3_baseline.csv', 'rt',
        #        encoding='utf-8', newline='') as src,
        print('Preparing to write in sheet2')
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
           
                # �����û��µ�½���������dictionary
                # ��ݣ�09|| 2009
                # �·�  2 || 12
                loginDaysDict = clientLoginEventUtility().getClientLoginDaysInYearMonth(19, 8)
            
                # src Ϊ�ȽϷ���
                """
                workbooksrc = xlrd.open_workbook('D:\DataTool\dataTool.xls')
                src = workbooksrc.sheet_by_name('Sheet3')
                """
                # �Ǽ��û��Զ��庯����db(д��sql�������ʱ����user-defined function raised exception)
                # db.create_function('checkMarketRelation',  4, CheckMarketRelation())

                workbookdes = xlwt.Workbook()
                dst = workbookdes.add_sheet('sheet2')

                sqStatement =  'SELECT newaccount.khdate, newaccount.khcode, newaccount.usrnameshort, newaccount.usrname,\
                        newaccount.khusrmobile, newaccount.lddepid, newaccount.lddepname,\
                        newaccount.marketperid, newaccount.qdbm, newaccount.tjrsj, newaccount.marketdepid,\
                        newaccount.marketpername, newaccount.marketpertype, newaccount.marketpermobile, newaccount.marketdepname \
                        FROM newaccount\
                            WHERE newaccount.tjrsj IS NOT NULL;'

                #̧ͷ����
                dst.write(0, 0, '����ʱ��')  #A
                dst.write(0, 1, '�����˺�')  #B
                dst.write(0, 2, '�ͻ����')  #C
                dst.write(0, 3, '�ͻ�����')  #D
                dst.write(0, 4, '�����ֻ���') #E
                dst.write(0, 5, '���µ�½����') #F
                dst.write(0, 6, '���Ӫҵ������') #G
                dst.write(0, 7, '���Ӫҵ������') #H
                dst.write(0, 8, 'Ӫ����Ա����') #I
                dst.write(0, 9, 'Ӫ����Ա����') #J
                dst.write(0, 10, 'Ӫ����Ա���') #K
                dst.write(0, 11, 'Ӫ����Ա�ֻ���') #L
                dst.write(0, 12, 'Ӫ��Ӫҵ������') #M
                dst.write(0, 13, 'Ӫ��Ӫҵ������') #N
                dst.write(0, 14, 'Ӫ����Ա���ǰԭֵ') #O
            
                row = 1
                for khdate, khcode, usrnameshort, usrname,\
                        khusrmobile, lddepid, lddepname,\
                        marketperid, qdbm, tjrsj, marketdepid,\
                        marketpername, marketpertype, marketpermobile, marketdepname\
                        in db.execute(sqStatement):
                
                    # CheckMarketRelation()
                    checkedMarketPerId = CheckMarketRelation.check(marketperid, qdbm, tjrsj, marketdepid)[0]
                    checkedMarketDepId = CheckMarketRelation.check(marketperid, qdbm, tjrsj, marketdepid)[1]
                    leavedMarketPerOriginalId =  CheckMarketRelation.check(marketperid, qdbm, tjrsj, marketdepid)[2]

                    checkedMarketDepName = None

                    ''''
                    if (str(checkedMarketPerId).strip() == 'None') or (str(checkedMarketPerId).strip() == ''):
                        # ���marketperid���������Ժ���ȻΪ��,˵��������ǻ��������¿���
                        if (str(checkedMarketPerId).strip() != '395000010066' ) and (str(checkedMarketPerId).strip() != '395000010065') and (str(checkedMarketPerId).strip() != '398000010900'):
                            self.internetReferUsers.append(str(khcode).strip())
                    '''

                    if (str(checkedMarketDepId).strip() == 'None') or (str(checkedMarketDepId).strip() == '') :
                        print('row: ' + str(row) + str(khusrmobile) + 'can not find market person and dep')
                    else:
                        for name in db.execute('SELECT marketdep.depname FROM marketdep WHERE marketdep.depid =?', (str(checkedMarketDepId),)):
                            checkedMarketDepName = name[0]
                 
                    dst.write(row, 0, str(khdate))
                    dst.write(row, 1, str(khcode))
                    dst.write(row, 2, str(usrnameshort))
                    dst.write(row, 3, str(usrname))
                    dst.write(row, 4, str(khusrmobile))
                
                    if str(khcode).strip() in loginDaysDict:
                        dst.write(row, 5, loginDaysDict[str(khcode).strip()])
                    else:
                        dst.write(row, 5, 0)

                    dst.write(row, 6, str(lddepid))
                    dst.write(row, 7, str(lddepname))
                
                    if str(khcode).strip() != '395000010066' and str(khcode).strip() != '395000010065' and str(khcode).strip() != '398000010900':
                        dst.write(row, 8, str(checkedMarketPerId))
                        dst.write(row, 9, str(marketpername))
                        dst.write(row, 10, str(marketpertype))
                        dst.write(row, 11, str(marketpermobile))
                        dst.write(row, 12, str(checkedMarketDepId))
                        dst.write(row, 13, str(checkedMarketDepName))

                        #leavedMarketPeriOriginalId Ҫ������8λҪ������None
                        if len(str(leavedMarketPerOriginalId)) == 8:
                            # ˵�����Ӫ����Ա�Ѿ���ְ��
                            dst.write(row, 14, str(leavedMarketPerOriginalId) + ' ��ְ')
                        else:
                            # None
                            dst.write(row, 14, '')
               
                    else:
                        if str(khcode).strip() == '395000010066':
                            dst.write(row, 8,  "39708036")
                            dst.write(row, 9,  "����")
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
                            dst.write(row, 10,"�Ƹ�����ʦ")
                            dst.write(row, 11, "18247130746")
                            dst.write(row, 12, "3780")
                            dst.write(row, 13,"3780 ���ͺ�����ɽ��·֤ȯӪҵ��")
                    
                    row = row + 1

                workbookdes.save('../output/sheet2.xls')

                """
                return dataframe read from sheet2 
                """
                dfreturn = pd.read_excel('../output/sheet2.xls', sheetname='sheet2')
                print('return')
                print(dfreturn.columns)
                print(dfreturn)
                self.dataframe = dfreturn

        #update newaccount based on modified sheet2
        #updateNewAccount.update(self.dataframe)
        # ������߼������޸�newaccount�����ֵ������ɾ����ǰ�����ݣ�Ȼ���sheet2�ܳ����Ľ����ȫ���ȥ
        updateNewAccount.reimport(self.dataframe)
        updateLeftMarketPer.update(self.leftMarketPerIds)

    def getSheet2DataFrame(self):
        self.generateSheet2ExcelFromSQLite()
        return self.dataframe

    def getLeftMarketPerIDs(self):
        self.generateSheet2ExcelFromSQLite()
        return list(set(self.leftMarketPerIds))

    def getInternetReferUsers(self):
        self.generateSheet2ExcelFromSQLite()
        return self.internetReferUsers

# generate sheet2 excel
sheet2 = getSheet2FromSQLite()
result = sheet2.getInternetReferUsers()
print(len(result))
count = 0
for user in result:
    print(count)
    print(user)
    count = count + 1


#print(len(sheet2.getInternetReferUsers()))
# leftmarketpers = sheet2.getLeftMarketPerIDs()
# print(leftmarketpers)
# updateLeftMarketPer.update(leftmarketpers)
