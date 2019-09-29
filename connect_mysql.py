#!/usr/bin/env python
import pymysql

def conn(host, port, username, password, db):
    c = pymysql.connect(host=host, port=port, user=username, passwd=password, db=db)
    cursor = c.cursor()
    sql = 'show databases'
    cursor.execute(sql)
    result = cursor.fetchall()
    print result
    cursor.close()

if __name__ == '__main__':
    conn('127.0.0.1', 3306, 'root', 'r00t', 'mysql')

