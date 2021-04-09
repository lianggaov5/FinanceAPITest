# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/2/21 8:59
@Author   :John
@Email    :337901080@qq.com
@File     :handle_user.py
@Software :PyCharm
********************************
"""
from MyFinanceAPI.scripts.handle_request import HttpRequest
from MyFinanceAPI.scripts.handle_mysql import HandleMysql
from MyFinanceAPI.scripts.parser_config import ParserConfig
from MyFinanceAPI.scripts.constants import CONFIGS_FILE_PATH, USER_CONFIGS_FILE_PATH


def create_new_user(regname, pwd="123456"):
    """
    创建新的用户
    :param regname:
    :param pwd:
    :return:
    """
    do_config = ParserConfig(CONFIGS_FILE_PATH)
    url = do_config("api", "prefix_url")+r"/member/register"
    do_mysql = HandleMysql()
    new_tel = do_mysql.create_not_existed_tel()
    do_request = HttpRequest()
    do_request(method="post", url=url, data={"mobilephone": new_tel, "pwd": pwd})
    sql = "SELECT t.Id from member t WHERE t.MobilePhone = %s;"
    user_id = do_mysql(sql, args=(new_tel, ))["Id"]
    user_dict = {regname: {"id": user_id, "tel": new_tel, "pwd": pwd, "regname": regname}}
    do_mysql.close()
    do_request.close()
    return user_dict


def generate_user_config():
    """
    生成3个随机用户
    :return:
    """
    users_data_dict = {}
    users_data_dict.update(create_new_user("loan_user"))
    users_data_dict.update(create_new_user("admin_user"))
    users_data_dict.update(create_new_user("invest_user"))
    do_config = ParserConfig(USER_CONFIGS_FILE_PATH)
    do_config.write_to_config(users_data_dict)


if __name__ == '__main__':
    print(create_new_user("loan_user"))
    generate_user_config()
