# -*- coding:utf-8 -*-
__author__ = 'IanChen'
import pymysql

def main():
    MYSQL_HOST = "127.0.0.1"
    MYSQL_DBNAME = "zhihu"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1029384756"
    MYSQL_Port = "3306"
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME, port=3306,
                           charset="utf8")
    cursor = conn.cursor()
    cursor.execute('select *from wangyi2 where id=3')
    rows=cursor.fetchall()
    print(rows[0][2])


if __name__ == "__main__":
    main()