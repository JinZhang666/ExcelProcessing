#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import csv
import xlrd
import xlwt
import pandas as pd

def playground3():
    workbookPath = '..\input\haha.xlsx'

    sheetName = 'Sheet2'

    df = pd.read_excel(workbookPath, sheet_name=sheetName)

    df1 = df['MOBILE'].values
    print(df1.size)

    with sqlite3.connect('C:\sqlite\db\hxdata.db') as db:
        sqStatement = 'SELECT mobile FROM inertialtesters'
        results = []


playground3()