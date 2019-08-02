#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
from UpdateSQliteTables.updateNewAccount import *
from UpdateSQliteTables.updateLeftAccount import *
class updateAccount:

    def __init__(self):
        self.newAccounts = []
        self.accounts = []
        self.leftaccounts = []
        self.realnewaccounts = []
        self.initializeLeftAccounts()
        self.initializeRealNewAccounts()

    def initializeAccounts(self):
        self.Accounts = []
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            select_account_template = "SELECT khcode FROM account;"
            for khcode in db.execute(select_account_template):
                s = str(khcode).strip().replace('(', '').replace(',', '').replace(')', '')
                self.accounts.append(s)
                #print(s)

    def initializeNewAccounts(self):
        self.newAccounts = []
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
            select_newaccount_template = "SELECT khcode FROM newaccount;"
            for khcode1 in db.execute(select_newaccount_template):
                s1 = str(khcode1).strip().replace('(', '').replace(',', '').replace(')', '')
                self.newAccounts.append(s1)
                #print(s1)

    def initializeLeftAccounts(self):
        self.leftaccounts = []
        # 找出存在于account 却不存在于newaccount里的leftaccount
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:

            select_account_template = "SELECT khcode FROM account;"
            self.initializeNewAccounts()

            for khcode in db.execute(select_account_template):
                s = str(khcode).strip().replace('(','').replace(',','').replace(')','')
                if s not in self.newAccounts:
                    self.leftaccounts.append(s)
        #updateLeftAccount.update(self.leftaccounts)
        #print(self.leftaccounts)


    def initializeRealNewAccounts(self):
        self.realnewaccounts = []
        # 找出存在于newaccount 却不存在于account里的realnewaccount
        with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:

            select_newaccount_template = "SELECT khcode FROM newaccount;"
            self.initializeAccounts()

            for khcode in db.execute(select_newaccount_template):
                s = str(khcode).strip().replace('(', '').replace(',', '').replace(')', '')
                #print("initializerealnewaccounts: s = ", s )
                #print(self.accounts)
                if s not in self.accounts:
                    self.realnewaccounts.append(s)
        #print(self.realnewaccounts)

    def getLeftAccounts(self):
        return self.leftaccounts

    def getRealNewAccounts(self):
        return self.realnewaccounts

#u = updateAccount()
#print(u.leftaccounts)
#print(u.realnewaccounts)