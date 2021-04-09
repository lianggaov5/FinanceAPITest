# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/2/20 16:29
@Author   :John
@Email    :337901080@qq.com
@File     :handle_parameter.py
@Software :PyCharm
********************************
"""
import re
from MyFinanceAPI.scripts.handle_mysql import HandleMysql
from MyFinanceAPI.scripts.parser_config import ParserConfig
from MyFinanceAPI.scripts.constants import USER_CONFIGS_FILE_PATH


class HandleParameter:
    """
    处理参数化
    """
    not_existed_tel_pattern = re.compile(r"\$\{not_existed_tel\}")
    invest_user_tel_pattern = re.compile(r"\$\{invest_user_tel\}")
    admin_user_tel_pattern = re.compile(r"\$\{admin_user_tel\}")
    loan_user_id_pattern = re.compile(r"\$\{loan_user_id\}")
    loan_id_pattern = re.compile(r"\$\{loan_id\}")
    invest_id_pattern = re.compile(r"\$\{invest_user_id\}")

    @classmethod
    def not_existed_tel_replace(cls, data):
        """替换参数化未注册的手机号"""
        do_mysql = HandleMysql()
        new_tel = do_mysql.create_not_existed_tel()
        if re.search(cls.not_existed_tel_pattern, data):
            data = re.sub(cls.not_existed_tel_pattern, new_tel, data)

        do_mysql.close()  # 关闭数据库连接
        return data

    @classmethod
    def existed_tel_replace(cls, data):
        """替换参数化已注册的手机号"""
        do_config = ParserConfig(USER_CONFIGS_FILE_PATH)
        invest_user_tel = do_config("invest_user", "tel")
        if re.search(cls.invest_user_tel_pattern, data):
            data = re.sub(cls.invest_user_tel_pattern, str(invest_user_tel), data)
        admin_user_tel = do_config("admin_user", "tel")
        if re.search(cls.admin_user_tel_pattern, data):
            data = re.sub(cls.admin_user_tel_pattern, str(admin_user_tel), data)

        return data

    @classmethod
    def loan_user_id_replace(cls, data):
        """
        借款用户id的替换
        :param data:
        :return:
        """
        do_config = ParserConfig(USER_CONFIGS_FILE_PATH)
        loan_user_id = do_config("loan_user", "id")
        if re.search(cls.loan_user_id_pattern, data):
            data = re.sub(cls.loan_user_id_pattern, str(loan_user_id), data)

        return data

    @classmethod
    def loan_id_replace(cls, data):
        """
        标id的替换
        :param data:
        :return:
        """

        if re.search(cls.loan_id_pattern, data):
            loan_id = getattr(cls, "loan_id")  # 局部变量
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)

        return data

    # @classmethod
    # def loan_id_replace(cls, data):
    #     """
    #     标id的替换
    #     :param data:
    #     :return:
    #     """
    #     do_config = ParserConfig(USER_CONFIGS_FILE_PATH)
    #     loan_user_id = do_config("loan_user", "id")
    #     sql = "SELECT t1.Id FROM loan t1 WHERE t1.MemberID=%s ORDER BY CreateTime DESC LIMIT 0, 1;"
    #     do_mysql = HandleMysql()
    #     loan_id = do_mysql(sql, args=(loan_user_id,))["Id"]
    #     if re.search(cls.loan_id_pattern, data):
    #         data = re.sub(cls.loan_id_pattern, str(loan_id), data)
    #     do_mysql.close()
    #     return data

    @classmethod
    def invest_user_id_replace(cls, data):
        """
        投资用户id的替换
        :param data:
        :return:
        """
        do_config = ParserConfig(USER_CONFIGS_FILE_PATH)
        invest_id = do_config("invest_user", "id")
        if re.search(cls.invest_id_pattern, data):
            data = re.sub(cls.invest_id_pattern, str(invest_id), data)
        return data

    @classmethod
    def register_parameter(cls, data):
        """
        实现注册功能的参数化
        :param data:
        :return:
        """
        data = cls.not_existed_tel_replace(data)
        data = cls.existed_tel_replace(data)
        return data

    @classmethod
    def login_parameter(cls, data):
        """
        实现登录功能的参数化
        :param data:
        :return:
        """
        data = cls.not_existed_tel_replace(data)
        data = cls.existed_tel_replace(data)
        return data

    @classmethod
    def recharge_parameter(cls, data):
        """
        实现充值功能的参数化
        :param data:
        :return:
        """
        data = cls.not_existed_tel_replace(data)
        data = cls.existed_tel_replace(data)
        return data

    @classmethod
    def add_parameter(cls, data):
        """
        实现加标功能的参数化
        :param data:
        :return:
        """
        data = cls.existed_tel_replace(data)
        data = cls.loan_user_id_replace(data)
        return data

    @classmethod
    def invest_parameter(cls, data):
        """
        实现投资功能的参数化
        :param data:
        :return:
        """
        data = cls.existed_tel_replace(data)
        data = cls.invest_user_id_replace(data)
        data = cls.loan_user_id_replace(data)
        data = cls.loan_id_replace(data)

        return data


if __name__ == '__main__':
    HandleParameter.loan_id = 32
    data1 = '{"mobilephone": "${not_existed_tel}","pwd": "Gl123456"}'
    data2 = '{"mobilephone": "${invest_user_tel}","pwd": "Gl123456"}'
    data3 = '{"memberId":${loan_user_id},"title":"买房","amount":10000,"loanRate":10.0,"' \
            'loanTerm":6,"loanDateType":0,"repaymemtWay":4,"biddingDays":3}'
    data4 = '{"id":${loan_id},"status":4}'
    data5 = '{"id":${invest_user_id}, "id":${loan_id}}'
    sql = 'SELECT t1.Id FROM loan t1 WHERE t1.MemberID=${loan_user_id} ORDER BY CreateTime DESC LIMIT 0, 1;'

    print(HandleParameter.register_parameter(data1))
    print(HandleParameter.login_parameter(data2))
    print(HandleParameter.recharge_parameter(data2))
    print(HandleParameter.add_parameter(data3))
    print(HandleParameter.invest_parameter(data4))
    print(HandleParameter.invest_parameter(data5))
    print(HandleParameter.loan_user_id_replace(sql))





