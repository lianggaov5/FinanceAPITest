# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/2/19 17:22
@Author   :John
@Email    :337901080@qq.com
@File     :handle_mysql.py
@Software :PyCharm
********************************
"""
import random
import pymysql

from MyFinanceAPI.scripts.parser_config import do_config
from MyFinanceAPI.scripts.handle_log import do_log


class HandleMysql:
    """
    处理MySql
    """
    def __init__(self):
        # 1.建立连接
        self.conn = pymysql.connect(host=do_config("mysql", "host"),
                                    port=do_config("mysql", "port"),
                                    user=do_config("mysql", "user"),
                                    password=str(do_config("mysql", "password")),  # 注意是字符串
                                    db=do_config("mysql", "db"),
                                    charset=do_config("mysql", "charset"),  # utf-8会报错
                                    cursorclass=pymysql.cursors.DictCursor)
        # 2.获取游标
        self.cursor = self.conn.cursor()

    def __call__(self, sql, args=None, is_more=False):
        """
        如果sql为查询，返回一条记录或多条记录，如果sql为非查询，则返回受影响的行数
        :param sql:查询sql或非查询sql
        :param args:sql语句的参数，为序列类型，默认为None
        :param is_more:默认为False, 当sql为查询时，默认返回一条记录
        :return:返回一条记录或多条记录或受影响的行数
        """
        # 3.执行sql
        try:
            self.cursor.execute(sql, args)
            if sql.split()[0].lower() == 'select':
                if is_more:
                    result = self.cursor.fetchall()
                else:
                    result = self.cursor.fetchone()
                return result
            # 4.事务提交
            else:
                self.conn.commit()
                return self.cursor.rowcount
        except Exception as e:
            do_log.error(e)
            self.conn.rollback()

    def close(self):
        # 5.关闭游标
        self.cursor.close()
        # 6.关闭连接
        self.conn.close()

    @staticmethod
    def create_tel():
        """
        生成一个符合格式的手机号
        :return:
        """
        pre_three = ["134", "135", "136", "137", "138", "139", "150", "151", "152", "157",
                     "158", "159", "187", "188", "130", "131", "132", "155", "156", "185",
                     "186", "145", "133", "153", "180", "181", "189"]
        last_eight = random.sample("0123456789", 8)
        return random.choice(pre_three) + ''.join(last_eight)

    def is_existed_tel(self, mobile):  # 添加一个mobile参数
        """
        判断给定的手机号在数据库中是否存在
        :param mobile: 待判断的手机号
        :return:存在返回True, 否则返回False
        """
        sql = "SELECT t.MobilePhone from `member` t WHERE t.MobilePhone = %s;"
        res = self(sql, args=(mobile,))
        if res:
            return True
        else:
            return False

    def create_not_existed_tel(self):
        """创建未注册的手机号"""
        while True:
            one_mobile = self.create_tel()
            res = self.is_existed_tel(one_mobile)
            if not res:
                break
        return one_mobile


if __name__ == '__main__':
    handle_mysql = HandleMysql()
    sql1 = 'select * from `member` m where RegName = %s'
    sql2 = 'update `member` set RegName = %s where RegName = %s;'
    res_01 = handle_mysql(sql1, args=('Tom_222',), is_more=False)
    res_02 = handle_mysql(sql2, args=("Tom_123456", "Tom_222"))
    # print(handle_mysql.create_not_existed_tel())
    handle_mysql.close()
    print(res_01)
    print(res_02)
    pass

