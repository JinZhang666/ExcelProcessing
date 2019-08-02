#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3  
import csv 
import xlrd  
import xlwt 

def getSheet3FromSQLite():

    # �����ݿ������Լ���Ҫʹ�õı���ĵ�
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
            
            #̧ͷ����
            dst.write(0, 0, 'ע��ʱ��')  #A
            dst.write(0, 1, '�û��ֻ���')  #B
            dst.write(0, 2, '����ģ�⽻������')  #C
            dst.write(0, 3, 'Ӫ��Ӫҵ������')  #D
            dst.write(0, 4, 'Ӫ��Ӫҵ������') #E
            dst.write(0, 5, 'Ӫ����Ա����') #F
            dst.write(0, 6, 'Ӫ����Ա����') #G
            dst.write(0, 7, 'Ӫ����Ա���') #H
            dst.write(0, 8, 'Ӫ����Ա�ֻ���') #I


            for createtime, usrmobile, tradedays, departmentid, departmentname, marketcode, marketname, markettype, marketmobile in db.execute(sqStatement):
                
                dst.write(row, 0, str(createtime).split(' ')[0])
                dst.write(row, 1, str(usrmobile))  
                
                # ��Ϊ�õ��������ǻ���newreg��ʹ��simtrade�е�tradedays�ҵ����û���ģ�⽻������
                # �õ�None˵�����û���δ��ģ�⽻�׵ļ�¼, �ո�
                if str(tradedays).strip() == 'None':
                    dst.write(row, 2, '') 
                else:
                    dst.write(row, 2, str(tradedays))
                
                # ���û��Ӫ�����ű�ţ��ո�
                if str(departmentid).strip() == 'None':
                    dst.write(row, 3, '')
                else:
                    dst.write(row, 3, str(departmentid))

                # ���û��Ӫ���������ƣ��ո�
                if str(departmentname).strip() == 'None': 
                    dst.write(row, 4, '')
                else:
                    dst.write(row, 4, str(departmentname)) 
                
                # ���û��Ӫ����Ա��ţ��ո�
                if str(marketcode).strip() == 'None':
                    dst.write(row, 5, '') 
                else:
                    dst.write(row, 5, str(marketcode))
                
                # ���û��Ӫ����Ա���ƣ��ո�
                if str(marketname).strip() == 'None': 
                    dst.write(row, 6, '') 
                else:
                    dst.write(row, 6, str(marketname)) 
                
                # ���û��Ӫ����Ա��𣬿ո�
                if str(markettype).strip() == 'None':
                    dst.write(row, 7, '') 
                else:
                    dst.write(row, 7, str(markettype))
                
                # ���û��Ӫ����Ա�ֻ����ո�
                if str(marketmobile).strip() == 'None':
                    dst.write(row, 8, '')
                else: 
                    dst.write(row, 8, str(marketmobile)) 
                
                row = row + 1

            workbookdes.save('../output/sheet3.xls') 

            # csv.writer(dst).writerows(db.execute(sqStatement))
            
            # �Ƚϻ����ļ�������ļ�
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
