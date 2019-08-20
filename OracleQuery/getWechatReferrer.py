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
结果为dictionary: {usermobile: [wechatReferrerId, wechatNickName, realName, referrerPhone]
'''

class getWechatReferrer:

    def __init__(self, df):
        '''
        把dataframe分类为
        （1） 营销人员编码4位/8位: df1
        （2） 营销人员是Null: df2
        '''
        print('Here is addsheet6wechatreferrer')
        df1 = df[(df['营销人编码'] != 'None') & ((df['营销人编码'].str.len() == 4) | (df['营销人编码'].str.len() == 8))]
        df2 = df[df['营销人编码'] == 'None']
        totalrow = df1.shape[0] + df2.shape[0]
        if totalrow == df.shape[0]:
            print('data classification successfully!')

        self.f2fDic = self.getf2fReferrer(df1)
        if 18065051780 in self.f2fDic:
            print('18065051780 is in f2fDic')
        if 13721099224 in self.f2fDic:
            print('13721099224 is in f2fDic')
        self.posterDic = self.getPosterReferrer(df2)
        self.activityDic = self.getActivityReferrer(df2)
        self.totalDic = self.mergeDic(self.f2fDic, self.posterDic, self.activityDic)
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
    def mergeDic(self, dic1, dic2, dic3):
        print("merging dic")
        mergedDic = {}
        for user_phone in dic1:
            if user_phone in mergedDic:
                print("ERROR: user has multiple referrer!")
            else:
                dic = {}
                dic['REFERRER_ID'] = dic1[user_phone][2]
                dic['海报id'] = dic1[user_phone][3]
                dic['推荐渠道'] = 'f2f'
                mergedDic[user_phone] = dic

        for user_phone in dic2:
            if user_phone in mergedDic:
                print("ERROR: user has multiple referrer!")
            else:
                dic = {}
                dic['REFERRER_ID'] = dic2[user_phone][2]
                dic['海报id'] = dic2[user_phone][3]
                dic['推荐渠道'] = 'poster'
                mergedDic[user_phone] = dic

        for user_phone in dic3:
            if user_phone in mergedDic:
                print("ERROR: user has multiple referrer!")
            else:
                dic = {}
                dic['REFERRER_ID'] = dic3[user_phone][2]
                dic['海报id'] = dic3[user_phone][3]
                dic['推荐渠道'] = 'activity'
                mergedDic[user_phone] = dic

        return mergedDic

    def getf2fReferrer(self, df1):
        print("getting f2f referrer...")
        f2fDic = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            print('The ip is :' + '10.189.65.81')
            df3 = df1[['营销人编码', '开户手机号']]
            cur = db.cursor()
            for key, value in df3.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, sns_user_id, page_index FROM t1_f2f_referrer WHERE market_code=:1 and user_phone=:2',

                    (value['营销人编码'], value['开户手机号']))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                # 上面已经筛选，不可能出现重复的用户
                if value['开户手机号'] == 18065051780 or value['开户手机号'] == 13721099224:
                    print('-----------------------------------')
                    print(res)
                    print(resEarliest)
                    print('-----------------------------------')

                if len(resEarliest) > 0:
                    f2fDic[value['开户手机号']] = resEarliest[0]


        return f2fDic
        # print(f2fDic)
        # print(len(f2fDic.keys()))

    def getPosterReferrer(self, df2):
        print("getting poster referrer...")
        activityDic = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            df5 = df2[['营销人编码', '开户手机号']]
            cur = db.cursor()
            for key, value in df5.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, referrer_id, page_index FROM t1_referrer_user WHERE is_new_user = 1 and USER_PHONE=:1',
                    (value['开户手机号'],))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                '''
                print('-----------------------------------')
                print(res)
                print(resEarliest)
                print('-----------------------------------')
                '''
                if len(res) > 0:
                    activityDic[value['开户手机号']] = resEarliest[0]
        #print(activityDic)
        return activityDic

    def getActivityReferrer(self, df2):
        print("getting activity referrer...")
        posterDic = {}
        with cx_Oracle.connect('APPUSER/APPUSER@10.189.65.81:1521/orcl') as db:
            df4 = df2[['营销人编码', '开户手机号']]
            cur = db.cursor()
            for key, value in df4.iterrows():
                cur.execute(
                    'SELECT user_phone, create_time, referrer_id, page_index FROM t1_activity_referrer_user WHERE is_new_user = 1 and USER_PHONE=:1',
                    (value['开户手机号'],))
                res = cur.fetchall()
                resEarliest = self.getEarliestRecord(res)
                '''
                print('-----------------------------------')
                print(res)
                print(resEarliest)
                print('-----------------------------------')
                '''
                if len(res) > 0:
                    posterDic[value['开户手机号']] = resEarliest[0]
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
            # 查找到了两条记录，取更早的那一条
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

