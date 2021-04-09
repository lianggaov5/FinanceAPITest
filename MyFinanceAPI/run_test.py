# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/1/27 14:09
@Author   :John
@Email    :337901080@qq.com
@File     :run_test.py
@Software :PyCharm
********************************
"""
import os
import unittest
from datetime import datetime

from MyFinanceAPI.libs.HTMLTestRunnerNew import HTMLTestRunner
from MyFinanceAPI.scripts.parser_config import do_config
from MyFinanceAPI.scripts.constants import REPORTS_DIR
from MyFinanceAPI.scripts.constants import CASES_DIR
from MyFinanceAPI.scripts.constants import USER_CONFIGS_FILE_PATH
from MyFinanceAPI.scripts.handle_user import generate_user_config

if not os.path.exists(USER_CONFIGS_FILE_PATH):
    generate_user_config()


one_suite = unittest.defaultTestLoader.discover(CASES_DIR)
report_name = os.path.join(REPORTS_DIR, do_config("report", "report_name"))

# full_html_report_name = report_name+"_"+datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")+".html"
full_html_report_name = report_name+"_"+datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")+".html"
with open(full_html_report_name, mode="wb") as file:
    one_runner = HTMLTestRunner(stream=file,
                                verbosity=do_config("report", "verbosity"),
                                title=do_config("report", "title"),
                                description=do_config("report", "description"),
                                tester=do_config("report", "tester"))
    one_runner.run(one_suite)

