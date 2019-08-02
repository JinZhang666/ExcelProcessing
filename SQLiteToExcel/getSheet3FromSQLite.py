#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3  
import csv 
import xlrd  
import xlwt 

def getSheet3FromSQLite():

    # 打开数据库连接以及需要使用的表格文档
    # open('sheet3_baseline.csv', 'rt',
    #        encoding='utf-8', newline='') as src, 
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db: 
            
            workbooksrc = xlrd.open_workbook('D:\DataTool\dataTool.xls')
            src = workbooksrc.sheet_by_name('Sheet3')

            workbookdes = xlwt.Workbook() 
            dst = workbookdes.add_sheet('sheet3') 

            sqStatement =  'SELECT newreg.createtime, newreg.usrmobile, simtrade.tradedays, \
                                          newreg.departmentid, marketdep.depname, newreg.marketcode, \
                                          marketper.marketname, marketper.markettype, marketper.marketmobile\
                        FROM newreg \
                        LEFT JOIN simtrade \
                        ON newreg.usrmobile = simtrade.usrmobile \
                        LEFT JOIN marketdep \
                        ON newreg.departmentid = marketdep.depid \
                        LEFT JOIN marketper \
                        ON newreg.marketcode = marketper.marketcode \
                        ORDER BY newreg.createtime; '
            row = 1
            
            #抬头补充
            dst.write(0, 0, '注册时间')  #A
            dst.write(0, 1, '用户手机号')  #B
            dst.write(0, 2, '本月模拟交易天数')  #C
            dst.write(0, 3, '营销营业部代码')  #D
            dst.write(0, 4, '营销营业部名称') #E
            dst.write(0, 5, '营销人员编码') #F
            dst.write(0, 6, '营销人员名称') #G
            dst.write(0, 7, '营销人员类别') #H
            dst.write(0, 8, '营销人员手机号') #I


            for createtime, usrmobile, tradedays, departmentid, departmentname, marketcode, marketname, markettype, marketmobile in db.execute(sqStatement):
                
                dst.write(row, 0, str(createtime).split(' ')[0])
                dst.write(row, 1, str(usrmobile))  
                
                # 因为得到的数据是基于newreg，使用simtrade中的tradedays找到新用户的模拟交易天数
                # 得到None说明该用户尚未有模拟交易的记录, 空格
                if str(tradedays).strip() == 'None':
                    dst.write(row, 2, '') 
                else:
                    dst.write(row, 2, str(tradedays))
                
                # 如果没有营销部门编号，空格
                if str(departmentid).strip() == 'None':
                    dst.write(row, 3, '')
                else:
                    dst.write(row, 3, str(departmentid))

                # 如果没有营销部们名称，空格
                if str(departmentname).strip() == 'None': 
                    dst.write(row, 4, '')
                else:
                    dst.write(row, 4, str(departmentname)) 
                
                # 如果没有营销人员编号，空格
                if str(marketcode).strip() == 'None':
                    dst.write(row, 5, '') 
                else:
                    dst.write(row, 5, str(marketcode))
                
                # 如果没有营销人员名称，空格
                if str(marketname).strip() == 'None': 
                    dst.write(row, 6, '') 
                else:
                    dst.write(row, 6, str(marketname)) 
                
                # 如果没有营销人员类别，空格
                if str(markettype).strip() == 'None':
                    dst.write(row, 7, '') 
                else:
                    dst.write(row, 7, str(markettype))
                
                # 如果没有营销人员手机，空格
                if str(marketmobile).strip() == 'None':
                    dst.write(row, 8, '')
                else: 
                    dst.write(row, 8, str(marketmobile)) 
                
                row = row + 1

            workbookdes.save('../output/sheet3.xls') 

            # csv.writer(dst).writerows(db.execute(sqStatement))
            
            # 比较基础文件和输出文件
            """ 
            dst.seek(0) 
            for line1, line2 in zip(range(src.nrows), dst):
                assert str(line1).rstrip() == str(line2).rstrip() 
            """


            """
            for usrmobile, marketcode, departmentid, createtime in db.execute(
                'SELECT usrmobile, marketcode, departmentid, createtime FROM newreg;'):
                print('%s %s %s %s' % (usrmobile, marketcode, departmentid, createtime))
            """

            """ 
            i = 0
            for usrmobile, tradedays in db.execute(
                'SELECT simtrade.usrmobile, simtrade.tradedays FROM simtrade INNER JOIN newreg ON simtrade.usrmobile = newreg.usrmobile;'): 
                print('%s %s' % (usrmobile, tradedays))
                i = i + 1

            print('%d' % (i))
            """
            
            """
            i = 0
            for createtime, usrmobile, tradedays, departmentid, departmentname, marketcode, marketname, markettype, marketmobile in db.execute(
                sqStatement): 
                print('%s %s %s %s %s %s %s %s %s' %(createtime, usrmobile, tradedays, departmentid, departmentname, marketcode, marketname, markettype, marketmobile))
                i = i + 1
            print('%d' % (i)) 
            """
getSheet3FromSQLite()
