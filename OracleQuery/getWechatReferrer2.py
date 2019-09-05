#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import pandas as pd
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#from SQLiteToExcel.getSheet6FromSQLite import *
'''
getwechatreferrer 
1. getf2fReferrer( df1 ) 
2, getPosterReferrer( df2 ) 
3. getActivityReferrer( df2 ) 
���Ϊdictionary: {usermobile: [wechatReferrerId, wechatNickName, realName, referrerPhone]
'''

class getWechatReferrer2:

    def __init__(self, df):
        '''
        ��dataframe����Ϊ
        ��1�� Ӫ����Ա����4λ/8λ: df1
        ��2�� Ӫ����Ա��Null: df2
        '''

        '''
        ?	���û����������е�Ӫ��������8λ����4λ������ҽ�Ӫ��Ӫҵ����ϵ������8λӪ������ҽ�Ӫ����Ա���ݺ�Ӫ��Ӫҵ�����ݣ������4λ��Ӫҵ������ҽ�Ӫ��Ӫҵ�����ݡ��ٸ����û��ֻ��š�Ӫ������������������ɨ���¼�ҽӻ�����������openID�����ж�Ӧ�Ķ��openID��¼ʱ��ȡ���ϵ�һ��Ϊ׼��
        ?	�������������Ӫ������Ϊ��
        ?	��1����ȡ�û��ֻ���+���Ӫҵ���������ɨ���¼�ҽӻ�����������openID, ���ж�Ӧ���openID��¼ʱ��ȡ���ϵ�һ��Ϊ׼��
        ?	��2�� ʣ��û�г����������ɨ���¼���û������û����������е�Ӫ������Ϊ�գ���ҽ�����Ӫ����ϵ�������û��ֻ��Ų���2.3.1��;��ע�����ݼ�Ӫ����ϵ��ֱ�ӹҽ��û���ע��ʱ��Ӫ����ϵ��Ӫ��΢��openid�������ID����
        '''

        print('Here is addsheet6wechatreferrer')
        df1 = df[(df['Ӫ���˱���'] != 'None') & ((df['Ӫ���˱���'].str.len() == 4) | (df['Ӫ���˱���'].str.len() == 8))]
        df2 = df[df['Ӫ���˱���'] == 'None']
        totalrow = df1.shape[0] + df2.shape[0]
        if totalrow == df.shape[0]:
            print('data classification successfully!')

        self.f2fDic1 = self.getf2fReferrerWithMarketCode(df1)
        self.f2fDic2 = self.getf2fReferrerWithourMarketCode(df2)
        self.posterDic = self.getPosterReferrer(df2)
        self.activityDic = self.getActivityReferrer(df2)
        self.totalDic = self.mergeDic(self.f2fDic1, self.f2fDic2, self.posterDic, self.activityDic)
        self.totalExpandedDic = self.getExpandedWechatReferrer(self.totalDic)

        '''
        for phone in self.totalExpandedDic:
            print(phone, self.totalExpandedDic[phone])
        print("total final record number: ", len(self.totalDic))
        '''

    def getFinalResult(self):
        return self.totalExpandedDic

    def getExpandedWechatReferrer(self, totalDic):
        print('getting expandedWechatReferrer')
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            cur = db.cursor()
            for user_phone in totalDic:
                totalDic[user_phone]['NICK_NAME'] = None
                totalDic[user_phone]['REAL_NAME'] = None
                totalDic[user_phone]['PHONE'] = None
                cur.execute(
                    'SELECT nick_name, real_name, phone FROM sns_user_info WHERE id=:1',
                    (totalDic[user_phone]['REFERRER_ID'],))
                res = cur.fetchall()
                for nick_name, real_name, phone in res:
                    totalDic[user_phone]['NICK_NAME'] = nick_name
                    totalDic[user_phone]['REAL_NAME'] = real_name
                    totalDic[user_phone]['PHONE'] = phone
        return totalDic

    # 13008449337 ('13008449337', datetime.datetime(2019, 4, 1, 10, 27, 30, 162000), '626161b2549d4f759c613b047101200a', None)
    def mergeDic(self, dic1, dic2, dic3, dic4):
        print("merging dic")
        mergedDic = {}

        '''
        dic1
        '''
        for user_phone in dic1:
            if user_phone in mergedDic:
                print("WARNING: user %d has multiple referrer!"%(user_phone))
            else:
                dic = {}
                dic['REFERRER_ID'] = dic1[user_phone][2]
                dic['����id'] = dic1[user_phone][3]
                dic['�Ƽ�����'] = 'f2fWithMarketCode'
                mergedDic[user_phone] = dic

        '''
        dic2 
        '''
        for user_phone in dic2:
            if user_phone in mergedDic:
                print("WARNING: user %d has multiple referrer!"%(user_phone))
            else:
                dic = {}
                dic['REFERRER_ID'] = dic2[user_phone][2]
                dic['����id'] = dic2[user_phone][3]
                dic['�Ƽ�����'] = 'f2fWithoutMarketCode'
                mergedDic[user_phone] = dic

        '''
        dic3
        '''
        for user_phone in dic3:
            if user_phone in mergedDic:
                print("WARNING: user %d has multiple referrer!"%(user_phone))
            else:
                dic = {}
                dic['REFERRER_ID'] = dic3[user_phone][2]
                dic['����id'] = dic3[user_phone][3]
                dic['�Ƽ�����'] = 'poster'
                mergedDic[user_phone] = dic

        for user_phone in dic4:
            if user_phone in mergedDic:
                print("WARNING: user %d has multiple referrer!"%(user_phone))
            else:
                dic = {}
                dic['REFERRER_ID'] = dic4[user_phone][2]
                dic['����id'] = dic4[user_phone][3]
                dic['�Ƽ�����'] = 'activity'
                mergedDic[user_phone] = dic

        return mergedDic

    def getf2fReferrerWithMarketCode(self, df1):
        print("getting f2f referrer with MarketCode...")
        f2fDic1 = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            print('The ip is :' + '10.189.65.81')
            df3 = df1[['Ӫ���˱���', '�����ֻ���']]
            cur = db.cursor()
            for key, value in df3.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, sns_user_id, page_index FROM t1_f2f_referrer WHERE market_code=:1 and user_phone=:2',

                    (value['Ӫ���˱���'], value['�����ֻ���']))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                # �����Ѿ�ɸѡ�������ܳ����ظ����û�
                if len(resEarliest) > 0:
                    f2fDic1[value['�����ֻ���']] = resEarliest[0]

        return f2fDic1

    def getf2fReferrerWithourMarketCode(self, df2):
        print("getting f2f referrer without MarketCode...")
        f2fDic2 = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            print('The ip is :' + '10.189.65.81')
            df3 = df2[['��ز�����', '�����ֻ���']]
            cur = db.cursor()
            for key, value in df3.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, sns_user_id, page_index FROM t1_f2f_referrer WHERE department_id=:1 and user_phone=:2',
                    (value['��ز�����'], value['�����ֻ���']))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                # �����Ѿ�ɸѡ�������ܳ����ظ����û�
                if len(resEarliest) > 0:
                    f2fDic2[value['�����ֻ���']] = resEarliest[0]
        return f2fDic2


    def getPosterReferrer(self, df2):
        print("getting poster referrer...")
        activityDic = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            df5 = df2[['Ӫ���˱���', '�����ֻ���']]
            cur = db.cursor()
            for key, value in df5.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, referrer_id, page_index FROM t1_referrer_user WHERE is_new_user = 1 and USER_PHONE=:1',
                    (value['�����ֻ���'],))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                '''
                print('-----------------------------------')
                print(res)
                print(resEarliest)
                print('-----------------------------------')
                '''
                if len(res) > 0:
                    activityDic[value['�����ֻ���']] = resEarliest[0]
        #print(activityDic)
        return activityDic

    def getActivityReferrer(self, df2):
        print("getting activity referrer...")
        posterDic = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            df4 = df2[['Ӫ���˱���', '�����ֻ���']]
            cur = db.cursor()
            for key, value in df4.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, referrer_id, page_index FROM t1_activity_referrer_user WHERE is_new_user = 1 and USER_PHONE=:1',
                    (value['�����ֻ���'],))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                '''
                print('-----------------------------------')
                print(res)
                print(resEarliest)
                print('-----------------------------------')
                '''
                if len(res) > 0:
                    posterDic[value['�����ֻ���']] = resEarliest[0]
        #print(posterDic)
        return posterDic

    # def mergeDic(self, f2fDic, posterDic, activityDic):

    def getEarliestRecord(self, res):
        timeCol = 1
        index = 0
        if len(res) == 0 or len(res) == 1:
            return res
        if len(res) > 1:
            # print(res)
            # ���ҵ���������¼��ȡ�������һ��
            datetime = res[0][timeCol]
            count = 0
            for record in res:
                if record[timeCol] < datetime:
                    datetime = record[timeCol]
                    index = count
                count = count + 1

        # print(res[index][3])
        resreturn = []
        resreturn.append(res[index])
        return resreturn

