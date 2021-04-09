# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/2/19 18:42
@Author   :John
@Email    :337901080@qq.com
@File     :constants.py
@Software :PyCharm
********************************
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 目录
# 存放脚本的目录
CASES_DIR = os.path.join(BASE_DIR, "cases")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
CONFIGS_DIR = os.path.join(BASE_DIR, "configs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DATAS_DIR = os.path.join(BASE_DIR, "datas")
LIBS_DIR = os.path.join(BASE_DIR, "libs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# 路径
CONFIGS_FILE_PATH = os.path.join(CONFIGS_DIR, "test_case.conf")
DATAS_FILE_PATH = os.path.join(DATAS_DIR, "test_case.xlsx")
USER_CONFIGS_FILE_PATH = os.path.join(CONFIGS_DIR, "user_accounts.ini")

pass
