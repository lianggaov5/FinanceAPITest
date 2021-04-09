# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/1/27 10:45
@Author   :John
@Email    :337901080@qq.com
@File     :handle_log.py
@Software :PyCharm
********************************
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from MyFinanceAPI.scripts.parser_config import do_config
from MyFinanceAPI.scripts.constants import LOGS_DIR


class HandleLog:
    """
    封装日志记录器
    """

    def __init__(self):
        self.case_logger = logging.getLogger(do_config("log", "logger_name"))
        self.case_logger.setLevel(do_config("log", "logger_level"))
        console_handle = logging.StreamHandler()
        file_handle = RotatingFileHandler(os.path.join(LOGS_DIR, do_config("file_path", "log_path")),
                                          maxBytes=3*1024*do_config("log", "maxBytes"),
                                          backupCount=do_config("log", "backupCount"),
                                          encoding="utf-8")
        console_handle.setLevel("ERROR")
        file_handle.setLevel("INFO")
        simple_formatter = logging.Formatter(do_config("log", "simple_formatter"))
        common_formatter = logging.Formatter(do_config("log", "common_formatter"))
        console_handle.setFormatter(simple_formatter)
        file_handle.setFormatter(common_formatter)
        self.case_logger.addHandler(console_handle)
        self.case_logger.addHandler(file_handle)

    # @property
    def get_logger(self):
        return self.case_logger


do_log = HandleLog().get_logger()

if __name__ == '__main__':
    do_log = HandleLog().get_logger()
    do_log.debug("这是debug")
    do_log.info("这是info")
    do_log.error("这是错误信息")
