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
2. 拿到sheet2 
3. 根据sheet2去update newacc 
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

        # checkMarketRelation 函数检查营销人员编号是不是填写，如果没有填写，用以下方法找【离职人员的营销关系】：
        # 1. 查看QDBM字段
        # 1）如果该字段是以'_'隔开的形式，那么被隔开的第3个字符串, 可能是空字符串/4位营销编码/8位营销编码，如果是一个8位的营销人员编码，则说明该人员因为离职才没有填写，营销人员编码直接写营销部代码;
        # * marketperid = 该字段前4位编码
        # * marketdepid = 该字段前4位编码
        # * marketdepname = 营销营业部代码对应的营销部名称（在input/《营销人员和营业部列表》excel的branchlist表单中查找到对应的支行名称 //在db的marketdep表中查找）
        # 2）如果QDBM字段中找不到这个8位的营销编码
        #       2.查看newacc表格中TJRSJ字段
        #       1）如果该字段是8位编码，那么说明这个员工已经离职，营销人员编码直接写写营业部代码：
        #       * marketperid = 该字段的前4位编码
        #       * marketdepid = 该字段的前4位编码
        #       * marketdepname = 营销营业部代码对应的营销部名称（在input/《营销人员和营业部列表》excel的branchlist表单中查找到对应的支行名称 //在db的marketdep表中查找）
        #       2）如果不是8位编码，什么都不做，marketperid, marketdepid, marketdepname 都空着
    
        class CheckMarketRelation:
            """ 用于补充营销关系 """
            """ return: 1. 营销人员编码(marketperid) 2. 营销营业部编码(marketdepid)"""
        
            def check(marketperid, qdbm, tjrsj, marketdepid):
            
                #print('Here is checkMarketrelation')
                mpi = marketperid
                mdi = marketdepid
                mpiOriginal = None
                #print('checkMarketRelation 1')
           
                if marketperid is None:
                    #print('marketperid is none')
                
                    try:
                        #查QDBM
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
                            mpi = str(qdbm).split('_')[2] #被'_'隔开的第3个字符串赋给mpi,可能是4位数，也可能位空，也可能是8位
                            if len(str(qdbm).split('_')[2]) == 8:

                                #register leftperid
                                self.leftMarketPerIds.append(str(qdbm).split('_')[2])

                                mpi = str(qdbm).split('_')[2][0:4]
                                mpiOriginal = str(qdbm).split('_')[2]
                            mdi = mpi
                
                        else:
                            #查TJRSJ
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

                #mpiOriginal一定是8位的
                return str(mpi), str(mdi), str(mpiOriginal)


        # 打开数据库连接以及需要使用的表格文档
        # open('sheet3_baseline.csv', 'rt',
        #        encoding='utf-8', newline='') as src,
        print('Preparing to write in sheet2')
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
           
                # 补充用户月登陆天数所需的dictionary
                # 年份：09|| 2009
                # 月份  2 || 12
                loginDaysDict = clientLoginEventUtility().getClientLoginDaysInYearMonth(19, 8)
            
                # src 为比较范本
                """
                workbooksrc = xlrd.open_workbook('D:\DataTool\dataTool.xls')
                src = workbooksrc.sheet_by_name('Sheet3')
                """
                # 登记用户自定义函数到db(写在sql语句中暂时报错：user-defined function raised exception)
                # db.create_function('checkMarketRelation',  4, CheckMarketRelation())

                workbookdes = xlwt.Workbook()
                dst = workbookdes.add_sheet('sheet2')

                sqStatement =  'SELECT newaccount.khdate, newaccount.khcode, newaccount.usrnameshort, newaccount.usrname,\
                        newaccount.khusrmobile, newaccount.lddepid, newaccount.lddepname,\
                        newaccount.marketperid, newaccount.qdbm, newaccount.tjrsj, newaccount.marketdepid,\
                        newaccount.marketpername, newaccount.marketpertype, newaccount.marketpermobile, newaccount.marketdepname \
                        FROM newaccount\
                            WHERE newaccount.tjrsj IS NOT NULL;'

                #抬头补充
                dst.write(0, 0, '开户时间')  #A
                dst.write(0, 1, '交易账号')  #B
                dst.write(0, 2, '客户简称')  #C
                dst.write(0, 3, '客户名称')  #D
                dst.write(0, 4, '开户手机号') #E
                dst.write(0, 5, '本月登陆天数') #F
                dst.write(0, 6, '落地营业部代码') #G
                dst.write(0, 7, '落地营业部名称') #H
                dst.write(0, 8, '营销人员编码') #I
                dst.write(0, 9, '营销人员名称') #J
                dst.write(0, 10, '营销人员类别') #K
                dst.write(0, 11, '营销人员手机号') #L
                dst.write(0, 12, '营销营业部代码') #M
                dst.write(0, 13, '营销营业部名称') #N
                dst.write(0, 14, '营销人员变更前原值') #O
            
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
                        # 如果marketperid经过修正以后仍然为空,说明这个人是互联网拉新开户
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

                        #leavedMarketPeriOriginalId 要不就是8位要不就是None
                        if len(str(leavedMarketPerOriginalId)) == 8:
                            # 说明这个营销人员已经离职了
                            dst.write(row, 14, str(leavedMarketPerOriginalId) + ' 离职')
                        else:
                            # None
                            dst.write(row, 14, '')
               
                    else:
                        if str(khcode).strip() == '395000010066':
                            dst.write(row, 8,  "39708036")
                            dst.write(row, 9,  "陈凌")
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
                            dst.write(row, 10,"财富管理师")
                            dst.write(row, 11, "18247130746")
                            dst.write(row, 12, "3780")
                            dst.write(row, 13,"3780 呼和浩特中山西路证券营业部")
                    
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
        # 这里的逻辑不是修改newaccount里面的值，而是删除以前的数据，然后把sheet2跑出来的结果完全存进去
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
