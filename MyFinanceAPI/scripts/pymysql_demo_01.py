# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/4/8 13:29
@Author   :John
@Email    :337901080@qq.com
@File     :pymysql_demo_01.py
@Software :PyCharm
********************************
"""
import pymysql


connect = pymysql.connect(host="192.168.65.129",
                          port=3306,
                          user="root",
                          password="123456",
                          database="books",
                          charset="utf8",
                          autocommit=True
                          )
cursor = connect.cursor()


sql = "select * from `t_book` t;"
sql = 'insert t_book(id, title, pub_date)values(100, "西游记", "1986-01-01");'
# sql = 'update t_book set title="东游记" where id=5;'
# sql = 'delete from t_book where id=5;'
cursor.execute(sql)
sql_01 = 'insert t_book(id, title, pub_date)values(5, "西游记", "1986-01-01");'
sql_02 = 'insert t_hero(name, gender, descriptiong)values("杨过", 2, "黯然销魂掌");'
# result = cursor.fetchone()
# print(cursor.rownumber)

# connect.commit()
result = cursor.fetchall()
# print(cursor.rowcount)


cursor.close()
connect.close()


