#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Read staff information from excel
and insert into sqlite3
"""

import xlrd
import sqlite3
import sys
import os


def check_args(args):
    """
    check argument is given and this
    file is excel
    """
    if len(args) != 2:
        print "please input excel file path!"
        sys.exit(1)
    if not os.path.exists(args[1]):
        print "This file don't exists"
        sys.exit(1)


def read_excel(path):
    """
    get excel cell data and call insert_sql function.
    """
    data = xlrd.open_workbook(path)
    sheet = data.sheets()[0]
    nrows = sheet.nrows
    sql = "insert into user_info(username, pingyinname, email, \
office_num, mobile, department) values('%s', '%s', '%s', '%s', '%s', '%s')"
    for row in xrange(nrows):
        row += 2
        username = sheet.cell(row, 0).value
        pingyin = sheet.cell(row, 5).value
        email = sheet.cell(row, 3).value
        office = int(sheet.cell(row, 2).value)
        mobile = int(sheet.cell(row, 4).value)
        department = sheet.cell(row, 1).value
        _sql = sql % (username, pingyin, email, office, mobile, department)
        insert_sql(_sql)


def insert_sql(sql):
    db = sqlite3.connect("/data/work/constract/flaskr.db")
    cur = db.cursor()
    cx = cur.execute(sql)
    db.commit()
    db.close()

if __name__ == "__main__":
    check_args(sys.argv)
    read_excel(sys.argv[1])
