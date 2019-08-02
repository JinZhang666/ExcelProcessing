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

            sqStatement = "SELECT newreg.createtime, newreg.usrmobile, simtrade.tradedays, \
                                          newreg.departmentid, marketdep.depname, newreg.marketcode, \
                                          marketper.marketname, marketper.markettype, marketper.marketmobile,\
            newreg.refid, newreg.refnickname, newreg.refrealname, newreg.refphone, newreg.pageindex\
                        FROM newreg \
                        LEFT JOIN simtrade \
                        ON newreg.usrmobile = simtrade.usrmobile \
                        LEFT JOIN marketdep \
                        ON newreg.departmentid = marketdep.depid \
                        LEFT JOIN marketper \
                        ON newreg.marketcode = marketper.marketcode \
                        ORDER BY newreg.createtime; "
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

            dst.write(0, 9, '�Ƽ���id')
            dst.write(0, 10, '�Ƽ����ǳ�')
            dst.write(0, 11, '�Ƽ�������')
            dst.write(0, 12, '�Ƽ��˵绰')
            dst.write(0, 13, '����ID')

            for createtime, usrmobile, tradedays, departmentid, departmentname, marketcode, marketname, markettype, marketmobile,\
                refid, refnickname, refrealname, refphone, pageindex in db.execute(sqStatement):
                
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

                # expanded���õ���newreg�Դ�Ӫ����ϵ��
                if str(refid).strip() == 'None':
                    dst.write(row, 9, '')
                else:
                    dst.write(row, 9, str(refid))

                if str(refnickname).strip() == 'None':
                    dst.write(row, 10, '')
                else:
                    dst.write(row, 10, str(refnickname))

                if str(refrealname).strip() == 'None':
                    dst.write(row, 11, '')
                else:
                    dst.write(row, 11, str(refrealname))

                if str(refphone).strip() == 'None':
                    dst.write(row, 12, '')
                else:
                    dst.write(row, 12, str(refphone))

                if str(pageindex).strip() == 'None':
                    dst.write(row, 13, '')
                else:
                    dst.write(row, 13, str(pageindex))

                # iterator
                row = row + 1

            workbookdes.save('../output/expandedSheet3.xls')

            # csv.writer(dst).writerows(db.execute(sqStatement))

getSheet3FromSQLite()
