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

from MyFinanceAPI.libs.ddt import ddt, data
from MyFinanceAPI.scripts.parser_excel import ParserExcel
from MyFinanceAPI.scripts.parser_config import do_config
from MyFinanceAPI.scripts.handle_log import do_log
from MyFinanceAPI.scripts.handle_request import HttpRequest
from MyFinanceAPI.scripts.constants import LOGS_DIR, DATAS_FILE_PATH
from MyFinanceAPI.scripts.handle_parameter import HandleParameter


@ddt
class TestLogin(unittest.TestCase):
    """
    测试登录功能
    """
    parser_excel = ParserExcel(DATAS_FILE_PATH, sheet_name="login")
    case_list = parser_excel.get_cases()

    @classmethod
    def setUpClass(cls) -> None:
        """
        前置处理操作
        :return:
        """
        cls.filename = LOGS_DIR+r"\\"+do_config("file_path", "log_path")
        cls.file = open(cls.filename, mode="a", encoding="utf-8")
        do_log.info("{}".format("开始执行登录功能用例"))
        cls.do_request = HttpRequest()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        后置处理操作：
        :return:
        """
        do_log.info("{}".format("登录功能用例执行结束"))
        cls.do_request.close()

    @data(*case_list)
    def test_login(self, data_namedtuple):
        case_id = data_namedtuple.case_id+1
        title = data_namedtuple.title

        response = TestLogin.do_request(method=data_namedtuple.method,
                                        url=do_config("api", "prefix_url")+data_namedtuple.url,
                                        data=HandleParameter.login_parameter(data_namedtuple.data))

        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")

        try:
            self.assertEqual(data_namedtuple.expected, response.text, msg="测试【{}】失败".format(title))
        except AssertionError as e:
            do_log.error("{}，测试结果为：{}\n，具体异常信息为{}".format(title, run_fail_msg, e))
            self.parser_excel.write_result_to_excel(row=case_id, actual=response.text, result=run_fail_msg)
            raise e
        else:
            do_log.info("{},测试结果为：{}".format(title, run_success_msg))
            self.parser_excel.write_result_to_excel(row=case_id, actual=response.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()
