#!/usr/bin/python
# -*- coding: cp936 -*-

""" clientLoginEventUtility.py
��db�е�clientloginevent���������ݴ���
"""

import sqlite3  

class clientLoginEventUtility:
    """
    year: 19 
    month: 7
    """
    def __init__(self):
        self.dict5 = self.getClientLoginDaysInYearMonth(19, 5)
        self.dict6 = self.getClientLoginDaysInYearMonth(19, 6)
        self.dict7 = self.getClientLoginDaysInYearMonth(19, 7)
        self.dict8 = self.getClientLoginDaysInYearMonth(19, 8)

    # �ֵ䣬��¼ÿ���û��ܹ���¼������
    def getTotalLogginDays(self):
        myDict = {}
        resultDict = {}

        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            for clientid, logindate in db.execute("SELECT clientid, logindate FROM hisclientloginevent"):
                if clientid is not None:
                    if str(clientid).strip() in myDict:
                        if str(logindate).strip() in myDict[str(clientid).strip()]:
                            myDict[str(clientid).strip()][str(logindate).strip()] = myDict[str(clientid).strip()][str(logindate).strip()] + 1
                        else:
                            myDict[str(clientid).strip()][str(logindate).strip()] = 1
                    else:
                        myDict[str(clientid).strip()] = {}
                        myDict[str(clientid).strip()][str(logindate).strip()] = 1

        for key in myDict.keys():
            # clientid = khcode
            resultDict[str(key).strip()] = len(myDict[str(key).strip()])

        return resultDict



    # dic = {'name1' : {logindate: logintimes, logindate:logintimes}, 'name2': {...} ... }
    def getClientLoginDaysInYearMonth(self, year, month):
        
        y = None 
        m = None

        if len(str(year).strip()) == 2:
            y = '20' + str(year).strip() 
        else:
            if len(str(year).strip()) == 4:
                y = str(year).strip() 

        if len(str(month).strip()) == 1:
            m = '0' + str(month).strip() 
        else:
            if len(str(month).strip()) == 2:
                m = str(month).strip() 
        
        
        myDict = {}
        resultDict = {}

        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db: 
            for clientid, logindate in db.execute("SELECT clientid, logindate FROM\
            hisclientloginevent WHERE logindate LIKE ?", (str(y)+str(m)+'%',)):
                if clientid is not None:
                    if str(clientid).strip() in myDict:
                        if str(logindate).strip() in myDict[str(clientid).strip()]:
                            myDict[str(clientid).strip()][str(logindate).strip()] = myDict[str(clientid).strip()][str(logindate).strip()] + 1
                        else:
                            myDict[str(clientid).strip()][str(logindate).strip()] = 1
                    else:
                        myDict[str(clientid).strip()] = {}
                        myDict[str(clientid).strip()][str(logindate).strip()] = 1

        for key in myDict.keys():
            resultDict[str(key).strip()] = len(myDict[str(key).strip()])

        return resultDict

    '''
    �õ�ĳһ���û�����Ч��½�·�
    '''
    def getEffectiveLoginMonthByUser(self, khcode, usrmobile):
        print("getting " + str(khcode) +"effective login Month")
        #һ����һ���¼ӣ�ÿ�������궼checkһ���ǲ�����Ч��¼��
        khcode = str(khcode).strip()
        count = 0
        # 3��/4��
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            for COUNT in db.execute(  "SELECT COUNT FROM clientlogindays03150430 WHERE PHONE = ?", [usrmobile, ]):
                COUNT = int(str(COUNT).replace('(','').replace(')', '').replace(',', ''))
                count = count + COUNT
        if count >= 5:
            return '201904'

        # 5��
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            for COUNT1 in db.execute("SELECT COUNT FROM clientlogindays05010513 WHERE PHONE = ?", [usrmobile, ]):
                COUNT1 = int(str(COUNT1).replace('(','').replace(')', '').replace(',', ''))
                count = count + COUNT1
        if khcode in self.dict5:
            count = count + self.dict5[khcode]
        if count >= 5:
            return '201905'

        # 6�� - 8��
        if khcode in self.dict6:
            count = count + self.dict6[khcode]
        if count >= 5:
            return '201906'

        if khcode in self.dict7:
            count = count + self.dict7[khcode]
        if count >= 5:
            return '201907'

        if khcode in self.dict8:
            count = count + self.dict8[khcode]
        if count >= 5:
            return '201908'

        return None

    '''
    �õ���Ч��¼����¼������5�Σ����û��Լ���ﵽ��Ч��¼���·�
    '''
    '''
    def getEffectiveLoginUsersAndMonth(self):
       
        �õ�ÿ���µ��û���¼�������������5�쳢�Բ���effectivedict,������ھͲ�������
        ���û����5�죬�Ȳ���potentialeffectivedict���ȴ����������ʱ�����effectivedict, ���һ�κ�Ͳ�������
        
        effectivePhones = {}
        potentialEffectivePhones = {}

        effectiveUserIDs = {}
        #���º�����
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            for PHONE, COUNT in db.execute(
                    "SELECT PHONE, COUNT FROM clientlogindays03150430 WHERE COUNT >= 5"):
                if str(PHONE).strip() not in effectivePhones:
                    effectivePhones[str(PHONE).strip()] = '201904'

            for PHONE, COUNT in db.execute(
                    "SELECT PHONE, COUNT FROM clientlogindays03150430 WHERE COUNT < 5"):
                if str(PHONE).strip() not in effectivePhones:
                    effectivePhones[str(PHONE).strip()] = int(COUNT)

        #����
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            for PHONE, COUNT in db.execute(
                    "SELECT PHONE, COUNT FROM clientlogindays05010513 WHERE COUNT >= 5"):
                if str(PHONE).strip() not in effectivePhones:
                    effectivePhones[str(PHONE).strip()] = '201905'
            for PHONE, COUNT in db.execute(
                    "SELECT PHONE, COUNT FROM clientlogindays05010513 WHERE COUNT < 5"):
                if str(PHONE).strip() not in potentialEffectivePhones:
                    effectivePhones[str(PHONE).strip()] = int(COUNT)
                else:
                    potentialEffectivePhones[str(PHONE).strip()] = int(potentialEffectivePhones[str(PHONE).strip()]) + int(COUNT)

                if potentialEffectivePhones[str(PHONE).strip()] >= 5:
                    if str(PHONE).strip() not in effectivePhones:
                        effectivePhones[str(PHONE).strip()] = '201905'

            #������û���clientid, �����ǵ绰
            dict5 = clientLoginEventUtility.getClientLoginDaysInYearMonth(19, 5)
            for PHONE, COUNT in dict5:
                if COUNT >= 5:
                    if str(PHONE).strip() not in effectivePhones:
                        effectivePhones[str(PHONE).strip()] = '201905'
                else:
                    if str(PHONE).strip() not in potentialEffectivePhones:
                        effectivePhones[str(PHONE).strip()] = int(COUNT)
                    else:
                        potentialEffectivePhones[str(PHONE).strip()] = int(potentialEffectivePhones[str(PHONE).strip()]) + int(COUNT)

                #ͳ��potentialeffective�ļ���
                if potentialEffectivePhones[str(PHONE).strip()] >= 5:
                    if str(PHONE).strip() not in effectivePhones:
                        effectivePhones[str(PHONE).strip()] = '201905'

        #��������
            i = 6
            currentdict = None
            monthnow = 7
            while i <= monthnow:
                currentdict = clientLoginEventUtility.getClientLoginDaysInYearMonth(19, i)
                for PHONE, COUNT in currentdict:
                    if COUNT >= 5:
                        if str(PHONE).strip() not in effectivePhones:
                            effectivePhones[str(PHONE).strip()] = '20190' + monthnow
                    else:
                        if str(PHONE).strip() not in potentialEffectivePhones:
                            effectivePhones[str(PHONE).strip()] = int(COUNT)
                        else:
                            potentialEffectivePhones[str(PHONE).strip()] = int(
                                potentialEffectivePhones[str(PHONE).strip()]) + int(COUNT)

                    # ͳ��potentialeffective�ļ���
                    if potentialEffectivePhones[str(PHONE).strip()] >= 5:
                        if str(PHONE).strip() not in effectivePhones:
                            effectivePhones[str(PHONE).strip()] = '20190' + monthnow
        '''

# print(clientLoginEventUtility().getEffectiveLoginMonthByUser('369000011397', '15279727843'))
