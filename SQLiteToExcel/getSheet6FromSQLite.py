import sqlite3
import csv
import xlrd
import xlwt
from ExcelToSQLite.importAccountToSQlite import *
from ExcelToSQLite.importNewAccountToSQLite import *
from UpdateSQliteTables import updateAccount
from UpdateSQliteTables.updateAccount import *
from SQLiteToExcel.getSheet2FromSQLite import *
from SQLiteQuery.leftMarketPerQuery import *
from SQLiteQuery.newregQuery import *
from SQLiteDataProcessing.userDayInCapitalUtility import *
from SQLiteDataProcessing.clientTradeEventUtility import *
from SQLiteDataProcessing.userDayATradeUtility import *
from ExcelToSQLite.importCapitalToSQLite import *
from ExcelToSQLite.importTradeLogToSQLite import *
from ExcelToSQLite.importATradeToSQLite import *
from SQLiteDataProcessing.clientLoginEventUtility import  *
from ExcelToSQLite.importHisclientLoginEventToSQLite import *
from SQLiteQuery.newAccountQuery import  *
from ExcelToSQLite.importACCVALToSQLite import *
from SQLiteQuery.accValQuery import *

def getACCVALFromSQLite():
    # sheet6 accounts = sheet6注销的 + sheet6里出现但是在sheet2里找关系 + sheet2里记录的新用户
    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:

        '''
        更新account和newaccount表
        '''
        # import sheet 6(account) to account table
        #importAccountToSQLite()
        # import last acc+val 表格进入account table
        importAccountToSQLiteFromACCVAL()
        # import last acc+val 表格进入accval
        importAccValToSQLite()
        # import modified sheet2 to newaccount table
        getSheet2FromSQLite().generateSheet2ExcelFromSQLite() #把处理过的数据写到newaccount表里面, 同时更新leftaccount 和 leftmarketper
        # updateaccount 通过和newaccount的比较，分辨出leftaccounts 和 realnewaccounts
        ua = updateAccount()
        accvalquery = accValQuery()

        '''
        准备好各种转换率指标
        '''
        # 有效入金用户以及有效入金日期
        importCapitalToSQLite()
        effectiveCapticalUsersDict = userDayInCapitalUtility().geteffectiveCapitalUsersAndDates()
        #print(effectiveCapticalUsersDict)
        # 有效交易日期
        importTradeLogToSQLite()
        effectiveTradeUsersDict = clientTradeEventUtility().geteffectiveTradeUsersAndDates()
        print("effectiveTradeUsersDict", effectiveTradeUsersDict)
        # 有效跟投日期
        importATradeLogToSQLite()
        effectiveATradeUsersDict = userDayATradeUtility().geteffectiveATradeUsersAndDates()
        print("effectiveATradeUsersDict", effectiveATradeUsersDict)
        # 有效登录日期
        importHisClientLoginEventToSQLite()
        cl = clientLoginEventUtility()


        '''
        得到leftaccount的方式
            (1)sheet2中逻辑得到的leftaccount 
            (2)通过account 和 newaccount 的比较得出leftaccount ,并把他们upadate 到leftaccount 里
        '''
        leftaccounts = ua.getLeftAccounts()
        print('leftaccoutns', leftaccounts)
        updateLeftAccount.update(leftaccounts)

        realNewAccounts = ua.getRealNewAccounts()
        print('realNewAccounts', realNewAccounts)

        leftMarketPers = getAllLeftMarketPerIDs()
        print('leftMarketPers', leftMarketPers)

        una = newAccountQuery()
        leftMarketPersUsers = una.getAllLeftMarketPersUsers()
        print("leftMarketPersUsers", leftMarketPersUsers)


        # 抬头补充
        workbookdes = xlwt.Workbook()
        dst = workbookdes.add_sheet('ACC+VAL')

        dst.write(0, 0, '开户时间')  # A
        dst.write(0, 1, '交易账号')  # B
        dst.write(0, 2, '客户简称')  # C
        dst.write(0, 3, '开户手机号')  # D
        dst.write(0, 4, '有效跟投')  # E
        dst.write(0, 5, '跟投日期')  # F
        dst.write(0, 6, '有效登录')  # G
        dst.write(0, 7, '登录月份')  # H
        dst.write(0, 8, '有效入金')  # I
        dst.write(0, 9, '入金日期')  # I
        dst.write(0, 10, '有效交易')  # I
        dst.write(0, 11, '交易日期')  # I
        dst.write(0, 12, '价值')  # I
        dst.write(0, 13, '落地部代码')  # I
        dst.write(0, 14, '落地部名称')  # I
        dst.write(0, 15, '营销人编码')  # I
        dst.write(0, 16, '营销人名称')  # I
        dst.write(0, 17, '营销人类别')  # I
        dst.write(0, 18, '营销人手机')  # I
        dst.write(0, 19, '营销部代码')  # I
        dst.write(0, 20, '营销部名称')  # I
        dst.write(0, 21, '销户')  # I
        dst.write(0, 22, '离职')  # I
        dst.write(0, 23, '当月红包')  # I
        dst.write(0, 24, 'REFERRER_ID')
        dst.write(0, 25, 'NICK_NAME')  # I
        dst.write(0, 26, 'REAL_NAME')
        dst.write(0, 27, 'PHONE')  # I
        dst.write(0, 28, '海报id')  # I

        select_account_template = 'SELECT * FROM account'
        select_newaccount_template = 'SELECT * FROM newaccount WHERE khcode = ?'
        currentMonth: str = '07'
        nextMonth: str = '08'

        '''
        遍历整个account
        1) 是注销用户： 填入account里的值，并在’注销用户‘列标1
        2）不是足校用固话：填入newaccount里的值，并在’注销用户‘列不标值于最后，插入realnewAccounts 账号及其来自于 newaccount 的关联数据
        '''
        # 现在处理的哪一行数据
        row = 1
        for khcode, khdate, usrnameshort, usrname, khusrmobile, lddepid,\
                          lddepname, marketperid, marketpername, marketpertype, marketpermobile, marketdepname, marketdepid,\
                              hrid, tjrsj, qdbm in db.execute(select_account_template):

            # 看是不是注销用户
            #print(leftaccounts)
            #print(khcode)
            #print(('('+ str(khcode).strip() +',)') in leftaccounts)
            if (str(khcode).strip() in leftaccounts):
                # 红包
                redpocket = 0
                #print(row, "：processing left account")
                # 插入并高亮
                dst.write(row, 0, str(khdate))
                dst.write(row, 1, str(khcode))
                dst.write(row, 2, str(usrnameshort))
                dst.write(row, 3, str(khusrmobile))

                # flags
                effectiveatradeFlag = 0
                effectivetradeFlag = 0
                effectiveCapitalFlag = 0
                effectiveLoginFlag = 0

                # 有效跟投补充 #
                atradeDate = str(accvalquery.checkIfEffectiveATrade(str(khcode).strip())).strip()
                if atradeDate == 'None':
                    dst.write(row, 4, '0')
                    dst.write(row, 5, '')
                    ''''
                    if str(khcode).strip() in effectiveATradeUsersDict:
                        effectiveatradeFlag = 1
                        dst.write(row, 4, '1')
                        atradeDate = effectiveATradeUsersDict[str(khcode).strip()]
                        dst.write(row, 5, atradeDate)
                    else:
                        dst.write(row, 4, '0')
                        dst.write(row, 5, '')
                    '''
                else:
                    effectiveatradeFlag = 1
                    dst.write(row, 4, '1')
                    dst.write(row, 5, atradeDate)


                # 有效登录天数 #
                loginDate = str(accvalquery.checkIfEffectiveLogin(str(khcode).strip())).strip()
                if loginDate == 'None':
                    dst.write(row, 6, '0')
                    dst.write(row, 7, '')
                    ''''
                    loginDate = cl.getEffectiveLoginMonthByUser(khcode, khusrmobile)
                    if loginDate is not None:
                        effectiveLoginFlag = 1
                        dst.write(row, 6, '1')
                        dst.write(row, 7, loginDate)
                    else:
                        dst.write(row, 6, '0')
                        dst.write(row, 7, '')
                    '''
                else:
                    effectiveLoginFlag = 1
                    dst.write(row, 6, '1')
                    dst.write(row, 7, loginDate)

                # 有效入金补充 #
                capitaldate = str(accvalquery.checkIfEffectiveCapital(str(khcode).strip())).strip()
                if capitaldate == 'None':
                    dst.write(row, 8, '0')
                    dst.write(row, 9, '')
                    '''
                    if str(khcode).strip() in effectiveCapticalUsersDict:
                        effectiveCapitalFlag = 1
                        capitaldate = effectiveCapticalUsersDict[str(khcode).strip()]
                        dst.write(row, 8, '1')
                        dst.write(row, 9, capitaldate)
                    else:
                        dst.write(row, 8, '0')
                        dst.write(row, 9, '')
                    '''
                else:
                    effectiveCapitalFlag = 1
                    dst.write(row, 8, '1')
                    dst.write(row, 9, capitaldate)

                # 有效交易补充 #
                tradedate = str(accvalquery.checkIfEffectiveTrade(str(khcode).strip())).strip()
                if tradedate == 'None':
                    dst.write(row, 10, '0')
                    dst.write(row, 11, '')
                    '''
                    if str(khcode).strip() in effectiveTradeUsersDict:
                        effectivetradeFlag = 1
                        tradedate = effectiveTradeUsersDict[str(khcode).strip()]
                        dst.write(row, 10, '1')
                        dst.write(row, 11, tradedate)
                    else:
                        dst.write(row, 10, '0')
                        dst.write(row, 11, '')
                    '''
                else:
                    effectivetradeFlag = 1
                    dst.write(row, 10, '1')
                    dst.write(row, 11, tradedate)

                # 用户价值
                value = 0
                #
                if effectiveLoginFlag == 1:
                    value = value + 10
                if effectiveCapitalFlag == 1 or effectivetradeFlag == 1:
                    value = value + 20
                if effectiveatradeFlag == 1:
                    value = value + 50
                dst.write(row, 12, value)

                dst.write(row, 13, str(lddepid)) #N
                dst.write(row, 14, str(lddepname)) #O
                dst.write(row, 15, str(marketperid))  #P
                dst.write(row, 16, str(marketpername)) #Q
                dst.write(row, 17, str(marketpertype))  #R
                dst.write(row, 18, str(marketpermobile))  #S
                dst.write(row, 19, str(marketdepid)) #T
                dst.write(row, 20, str(marketdepname))  #U
                dst.write(row, 21, '1' ) #V #销户用户的高亮

                # 注销用户的离职人员没有办法判断，因为他们不存在于sheet2所以没法比较得出离职人员
                if str(marketperid).strip() in leftMarketPers:
                    # 如果用户对应的营销人员是已离职的营销人员
                    dst.write(row, 22, '1')  #W # 离职人员的高亮
                else:
                    dst.write(row, 22, '0')

                # 当月红包
                # 有效跟投 + 50
                if effectiveatradeFlag == 1:
                    if atradeDate[0:6] == "2019" + str(currentMonth).strip():
                        redpocket = redpocket + 50

                # 当月红包
                # 入金或者交易 + 20
                if (effectiveCapitalFlag == 1 and capitaldate[0:6] == "2019" + currentMonth and effectivetradeFlag == 0)\
                        or (effectivetradeFlag == 1 and tradedate[0:6] == '2019' + currentMonth and effectiveCapitalFlag == 0)\
                        or (effectiveCapitalFlag == 1 and effectivetradeFlag == 1 and capitaldate[0:6] == "2019" + currentMonth and tradedate[0:6] == '2019' + currentMonth)\
                    or (effectiveCapitalFlag == 1 and effectivetradeFlag == 1 and capitaldate[0:6] == "2019" + currentMonth  and tradedate[0:6] == '2019' + nextMonth)\
                    or (effectiveCapitalFlag == 1 and effectivetradeFlag == 1 and capitaldate[0:6] == "2019" + nextMonth  and tradedate[0:6] == '2019' + currentMonth):
                    redpocket = redpocket + 20

                # 当月红包
                # 有效登录+ 10
                if effectiveLoginFlag == 1:
                    if loginDate == "2019" + str(currentMonth).strip():
                        redpocket = redpocket + 10

                dst.write(row, 23, int(redpocket))

            else:
                #如果没有离开，找到该用户在sheet2的数据
                #print(row, ": processing exist account")
                leftMarketPerByCompare2and6 = []
                for khcode1, khdate1, usrnameshort1, usrname1, khusrmobile1, lddepid1,\
                          lddepname1, marketperid1, marketpername1, marketpertype1, marketpermobile1, marketdepname1, marketdepid1,\
                              hrid1, tjrsj1, qdbm1, isLeftMarketPer1 in db.execute(select_newaccount_template, [khcode,]):
                    redpocket1 = 0

                    #插入
                    # 插入并不高亮
                    dst.write(row, 0, str(khdate1))
                    dst.write(row, 1, str(khcode1))
                    dst.write(row, 2, str(usrnameshort1))
                    dst.write(row, 3, str(khusrmobile1))

                    # flags
                    effectiveatradeFlag1 = 0
                    effectivetradeFlag1 = 0
                    effectiveCapitalFlag1 = 0
                    effectiveLoginFlag1 = 0

                    # 有效跟投补充 #
                    atradeDate1 = str(accvalquery.checkIfEffectiveATrade(str(khcode1).strip())).strip()
                    if atradeDate1 == 'None':
                        if str(khcode1).strip() in effectiveATradeUsersDict:
                            effectiveatradeFlag1 = 1
                            dst.write(row, 4, '1')
                            atradeDate1 = effectiveATradeUsersDict[str(khcode1).strip()]
                            dst.write(row, 5, atradeDate1)
                        else:
                            dst.write(row, 4, '0')
                            dst.write(row, 5, '')
                    else:
                        effectiveatradeFlag1 = 1
                        dst.write(row, 4, '1')
                        dst.write(row, 5, atradeDate1)

                    # 有效登录天数 #
                    loginDate1 = str(accvalquery.checkIfEffectiveLogin(str(khcode1).strip())).strip()
                    if loginDate1 == 'None':
                        loginDate1 = cl.getEffectiveLoginMonthByUser(khcode1, khusrmobile1)
                        if loginDate1 is not None:
                            effectiveLoginFlag1 = 1
                            dst.write(row, 6, '1')
                            dst.write(row, 7, loginDate1)
                        else:
                            dst.write(row, 6, '0')
                            dst.write(row, 7, '')
                    else:
                        effectiveLoginFlag1 = 1
                        dst.write(row, 6, '1')
                        dst.write(row, 7, loginDate1)

                    # 有效入金补充 #
                    capitaldate1 = str(accvalquery.checkIfEffectiveCapital(str(khcode1).strip())).strip()
                    if capitaldate1 == 'None':
                        if str(khcode1).strip() in effectiveCapticalUsersDict:
                            effectiveCapitalFlag1 = 1
                            capitaldate1 = effectiveCapticalUsersDict[str(khcode1).strip()]
                            dst.write(row, 8, '1')
                            dst.write(row, 9, capitaldate1)
                        else:
                            dst.write(row, 8, '0')
                            dst.write(row, 9, '')
                    else:
                        effectiveCapitalFlag1 = 1
                        dst.write(row, 8, '1')
                        dst.write(row, 9, capitaldate1)

                    # 有效交易补充 #
                    tradedate1 = str(accvalquery.checkIfEffectiveTrade(str(khcode1).strip())).strip()
                    if tradedate1 == 'None':
                        if str(khcode1).strip() in effectiveTradeUsersDict:
                            effectivetradeFlag1 = 1
                            tradedate1 = effectiveTradeUsersDict[str(khcode1).strip()]
                            dst.write(row, 10, '1')
                            dst.write(row, 11, tradedate1)
                        else:
                            dst.write(row, 10, '0')
                            dst.write(row, 11, '')
                    else:
                        effectivetradeFlag1 = 1
                        dst.write(row, 10, '1')
                        dst.write(row, 11, tradedate1)

                    # 用户价值
                    value1 = 0
                    #
                    if effectiveLoginFlag1 == 1:
                        value1 = value1 + 10
                    if effectiveCapitalFlag1 == 1 or effectivetradeFlag1 == 1:
                        value1 = value1 + 20
                    if effectiveatradeFlag1 == 1:
                        value1 = value1 + 50
                    dst.write(row, 12, value1)

                    dst.write(row, 13, str(lddepid1))  # N
                    dst.write(row, 14, str(lddepname1))  # O
                    dst.write(row, 15, str(marketperid1))  # P
                    dst.write(row, 16, str(marketpername1))  # Q
                    dst.write(row, 17, str(marketpertype1))  # R
                    dst.write(row, 18, str(marketpermobile1))  # S
                    dst.write(row, 19, str(marketdepid1))  # T
                    dst.write(row, 20, str(marketdepname1))  # U
                    dst.write(row, 21, '0')  # V #销户用户的高亮

                    # print("marketperid", marketperid2)
                    # 因为sheet6里的数据也是以前sheet2覆盖而来，所以如果离职，并不能通过该行数据找到那个离职的人的号码
                    # 如果newacccount表里的'isLeftMarketPer'字段不为空，填1
                    if '(' + str(khcode1).strip() + ',)' in leftMarketPersUsers:
                        dst.write(row, 22, '1')
                    else:
                        dst.write(row, 22, '0')

                if len(leftMarketPerByCompare2and6) != 0:
                    updateLeftMarketPer.update(leftMarketPerByCompare2and6)

                # 当月红包
                # 有效跟投 + 50
                if effectiveatradeFlag1 == 1:
                    if atradeDate1[0:6] == "2019" + str(currentMonth).strip():
                        redpocket1 = redpocket1 + 50

                # 当月红包
                # 入金或者交易 + 20
                if (effectiveCapitalFlag1 == 1 and capitaldate1[0:6] == "2019" + currentMonth and effectivetradeFlag1 == 0)\
                        or (effectivetradeFlag1 == 1 and tradedate1[0:6] == '2019' + currentMonth and effectiveCapitalFlag1 == 0)\
                        or (effectiveCapitalFlag1 == 1 and effectivetradeFlag1 == 1 and capitaldate1[0:6] == "2019" + currentMonth\
                        and tradedate1[0:6] == '2019' + currentMonth)\
                        or (effectiveCapitalFlag1 == 1 and effectivetradeFlag1 == 1 and capitaldate1[0:6] == "2019" + currentMonth  and tradedate1[0:6] == '2019' + nextMonth)\
                        or (effectiveCapitalFlag1 == 1 and effectivetradeFlag1 == 1 and capitaldate1[0:6] == "2019" + nextMonth  and tradedate1[0:6] == '2019' + currentMonth):
                    redpocket1 = redpocket1 + 20

                # 当月红包
                # 有效登录+ 10
                if effectiveLoginFlag1 == 1:
                    if loginDate1 == "2019" + str(currentMonth).strip():
                        redpocket1 = redpocket1 + 10

                dst.write(row, 23, int(redpocket1))

            # iterator
            row = row + 1

         #遍历完成之后，补充不存在于account中的属于newaccount的用户
        print("realNewAccounts number is: ", len(realNewAccounts))
        for newkhcode in realNewAccounts:
            newkhcode = str(newkhcode).replace(",", "").replace(")", "").replace("(", "")

            #print("realnewaccount: ", newkhcode)
            for khcode2, khdate2, usrnameshort2, usrname2, khusrmobile2, lddepid2, \
                lddepname2, marketperid2, marketpername2, marketpertype2, marketpermobile2, marketdepname2, marketdepid2, \
                hrid2, tjrsj2, qdbm2, isLeftMarketPer2 in db.execute(select_newaccount_template, [newkhcode,]):
                #
                redpocket2 = 0

                #插入
                #print(row, "processing real new account")
                # 插入并高亮
                dst.write(row, 0, str(khdate2))
                dst.write(row, 1, str(khcode2))
                dst.write(row, 2, str(usrnameshort2))
                dst.write(row, 3, str(khusrmobile2))

                # flags
                effectiveatradeFlag2 = 0
                effectivetradeFlag2 = 0
                effectiveCapitalFlag2 = 0
                effectiveLoginFlag2 = 0

                # 有效跟投补充 #
                atradeDate2 = str(accvalquery.checkIfEffectiveATrade(str(khcode2).strip())).strip()
                if atradeDate2 == 'None':
                    if str(khcode2).strip() in effectiveATradeUsersDict:
                        effectiveatradeFlag2 = 1
                        dst.write(row, 4, '1')
                        atradeDate2 = effectiveATradeUsersDict[str(khcode2).strip()]
                        dst.write(row, 5, atradeDate2)
                    else:
                        dst.write(row, 4, '0')
                        dst.write(row, 5, '')
                else:
                    effectiveatradeFlag2 = 1
                    dst.write(row, 4, '1')
                    dst.write(row, 5, atradeDate2)


                # 有效登录天数 #
                loginDate2 = str(accvalquery.checkIfEffectiveLogin(str(khcode2).strip())).strip()
                if loginDate2 == 'None':
                    loginDate2 = cl.getEffectiveLoginMonthByUser(khcode2, khusrmobile2)
                    if loginDate2 is not None:
                        effectiveLoginFlag2 = 1
                        dst.write(row, 6, '1')
                        dst.write(row, 7, loginDate2)
                    else:
                        dst.write(row, 6, '0')
                        dst.write(row, 7, '')
                else:
                    effectiveLoginFlag2 = 1
                    dst.write(row, 6, '1')
                    dst.write(row, 7, loginDate2)

                # 有效入金补充 #
                capitaldate2 = str(accvalquery.checkIfEffectiveCapital(str(khcode2).strip())).strip()
                if capitaldate2 == 'None':
                    if str(khcode2).strip() in effectiveCapticalUsersDict:
                        effectiveCapitalFlag2 = 1
                        capitaldate2 = effectiveCapticalUsersDict[str(khcode2).strip()]
                        dst.write(row, 8, '1')
                        dst.write(row, 9, capitaldate2)
                    else:
                        dst.write(row, 8, '0')
                        dst.write(row, 9, '')
                else:
                    effectiveCapitalFlag2 = 1
                    dst.write(row, 8, '1')
                    dst.write(row, 9, capitaldate2)

                # 有效交易补充 #
                tradedate2 = str(accvalquery.checkIfEffectiveTrade(str(khcode2).strip())).strip()
                if tradedate2 == 'None':
                    if str(khcode2).strip() in effectiveTradeUsersDict:
                        effectivetradeFlag2 = 1
                        tradedate2 = effectiveTradeUsersDict[str(khcode2).strip()]
                        dst.write(row, 10, '1')
                        dst.write(row, 11, tradedate2)
                    else:
                        dst.write(row, 10, '0')
                        dst.write(row, 11, '')
                else:
                    effectivetradeFlag2 = 1
                    dst.write(row, 10, '1')
                    dst.write(row, 11, tradedate2)


                # 用户价值
                value2 = 0
                #
                if effectiveLoginFlag2 == 1:
                    value2 = value2 + 10
                if effectiveCapitalFlag2 == 1 or effectivetradeFlag2 == 1:
                    value2 = value2 + 20
                if effectiveatradeFlag1 == 1:
                    value2 = value2 + 50
                dst.write(row, 12, value2)


                dst.write(row, 13, str(lddepid2))  # N
                dst.write(row, 14, str(lddepname2))  # O
                dst.write(row, 15, str(marketperid2))  # P
                dst.write(row, 16, str(marketpername2))  # Q
                dst.write(row, 17, str(marketpertype2))  # R
                dst.write(row, 18, str(marketpermobile2))  # S
                dst.write(row, 19, str(marketdepid2))  # T
                dst.write(row, 20, str(marketdepname2))  # U
                dst.write(row, 21, '0')  # V #销户用户的高亮

                # 如果newacccount表里的'isLeftMarketPer'字段不为空，填1
                if '(' + str(khcode1).strip() + ',)' in leftMarketPersUsers:
                    dst.write(row, 22, '1')
                else:
                    dst.write(row, 22, '0')

                # 当月红包
                # 有效跟投 + 50
                if effectiveatradeFlag2 == 1:
                    if atradeDate2[0:6] == "2019" + str(currentMonth).strip():
                        redpocket2 = redpocket2 + 50

                # 当月红包
                # 入金或者交易 + 20
                if (effectiveCapitalFlag2 == 1 and capitaldate2[0:6] == "2019" + currentMonth and effectivetradeFlag2 == 0)\
                        or (effectivetradeFlag2 == 1 and tradedate2[0:6] == '2019' + currentMonth and effectiveCapitalFlag2 == 0)\
                        or (effectiveCapitalFlag2 == 1 and effectivetradeFlag2 == 1 and capitaldate2[0:6] == "2019" + currentMonth\
                        and tradedate2[0:6] == '2019' + currentMonth) \
                        or (effectiveCapitalFlag2 == 1 and effectivetradeFlag2 == 1 and capitaldate2[0:6] == "2019" + currentMonth and tradedate2[0:6] == '2019' + nextMonth) \
                        or (effectiveCapitalFlag2 == 1 and effectivetradeFlag2 == 1 and capitaldate2[0:6] == "2019" + nextMonth and tradedate2[0:6] == '2019' + currentMonth):
                    redpocket2 = redpocket2 + 20

                # 当月红包
                # 有效登录+ 10
                if effectiveLoginFlag2 == 1:
                    if loginDate2 == "2019" + str(currentMonth).strip():
                        redpocket2 = redpocket2 + 10


                dst.write(row, 23, int(redpocket2))

                # iterator
                row = row + 1

        print( 'inserted row is = ', row)
        workbookdes.save('../output/ACC+VAL.xls')
        dfreturn = pd.read_excel('../output/ACC+VAL.xls', sheetname='ACC+VAL')
        #print(dfreturn)
        return dfreturn

getACCVALFromSQLite()

'''
# 通过sheet6和sheet2的比较来得出离职人员（当期的）
marketperidFromNewAccount1 = None
marketperidFromAccount1 = None
for mpna1 in db.execute('SELECT marketperid FROM newaccount WHERE khcode = ?',
                        [khcode1,]):
    marketperidFromNewAccount1 = mpna1
for mpa1 in db.execute('SELECT marketperid FROM account WHERE khcode = ?',
                       [khcode1,]):
    marketperidFromAccount1 = mpa1


if str(marketperidFromAccount1).strip() == str(marketperidFromNewAccount1).strip() or\
        (str(marketperidFromAccount1).strip() == '(None,)' and str(marketperidFromNewAccount1).strip() == '(\'None\',)') or\
        (str(marketperidFromNewAccount1).strip() == '(None,)' and str(marketperidFromAccount1).strip() == '(\'None\',)'):
    dst.write(row, 22, '0')  # W # 离职人员的高亮
else:
    print("marketperidFromNewAccount1", marketperidFromNewAccount1)
    print("marketperidFromAccount1", marketperidFromAccount1)
    dst.write(row, 22, '1')
    leftMarketPerByCompare2and6.append(str(marketperidFromAccount1).strip())
'''