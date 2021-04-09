# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/1/25 18:54
@Author   :John
@Email    :337901080@qq.com
@File     :test_mul.py
@Software :PyCharm
********************************
"""
import unittest
import os

from MyFinanceAPI.libs.ddt import ddt, data
from MyFinanceAPI.scripts.parser_excel import ParserExcel
from MyFinanceAPI.scripts.parser_config import do_config
from MyFinanceAPI.scripts.handle_log import do_log
from MyFinanceAPI.scripts.handle_request import HttpRequest
from MyFinanceAPI.scripts.constants import LOGS_DIR, DATAS_FILE_PATH
from MyFinanceAPI.scripts.handle_parameter import HandleParameter
from MyFinanceAPI.scripts.handle_mysql import HandleMysql


@ddt
class TestInvest(unittest.TestCase):
    """
    测试投资功能
    """
    parser_excel = ParserExcel(DATAS_FILE_PATH, sheet_name="invest")
    case_list = parser_excel.get_cases()

    @classmethod
    def setUpClass(cls) -> None:
        cls.filename = os.path.join(LOGS_DIR, do_config("file_path", "log_path"))
        cls.file = open(cls.filename, mode="a", encoding="utf-8")
        do_log.info("{}".format("开始执行投资功能用例"))
        cls.do_request = HttpRequest()
        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls) -> None:
        do_log.info("{}".format("投资功能用例执行结束"))
        cls.do_request.close()
        cls.do_mysql.close()

    @data(*case_list)
    def test_invest(self, data_namedtuple):
        case_id = data_namedtuple.case_id+1
        title = data_namedtuple.title
        new_data = HandleParameter.invest_parameter(data_namedtuple.data)

        response = TestInvest.do_request(method=data_namedtuple.method,
                                         url=do_config("api", "prefix_url")+data_namedtuple.url,
                                         data=new_data)

        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")

        """反射"""
        if response.json().get("msg") == "加标成功":
            check_sql = data_namedtuple.check_sql
            if check_sql:
                check_sql = HandleParameter.invest_parameter(check_sql)
                sql_data = TestInvest.do_mysql(sql=check_sql)
                HandleParameter.loan_id = sql_data.get("Id")
                # setattr(HandleParameter, "loan_id", loan_id)

        try:
            self.assertEqual(data_namedtuple.expected, response.text, msg="测试【{}】失败".format(title))
        except AssertionError as e:
            do_log.error("{}，测试结果为：{}\n，具体异常信息为{}".format(title, run_fail_msg, e))
            self.parser_excel.write_result_to_excel(row=case_id, actual=response.text, result=run_fail_msg)
            raise e
        else:
            do_log.info("{},测试结果为：{}".format(title, run_success_msg))
            print("{}: {}".format(type(response.text), response.text))
            self.parser_excel.write_result_to_excel(row=case_id, actual=response.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()

