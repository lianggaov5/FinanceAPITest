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
import json
import unittest

from MyFinanceAPI.libs.ddt import ddt, data
from MyFinanceAPI.scripts.handle_mysql import HandleMysql
from MyFinanceAPI.scripts.parser_excel import ParserExcel
from MyFinanceAPI.scripts.parser_config import do_config
from MyFinanceAPI.scripts.handle_log import do_log
from MyFinanceAPI.scripts.handle_request import HttpRequest
from MyFinanceAPI.scripts.constants import LOGS_DIR, DATAS_FILE_PATH
from MyFinanceAPI.scripts.handle_parameter import HandleParameter


@ddt
class TestRecharge(unittest.TestCase):
    """
    测试充值功能
    """
    parser_excel = ParserExcel(DATAS_FILE_PATH, sheet_name="recharge")
    case_list = parser_excel.get_cases()

    @classmethod
    def setUpClass(cls) -> None:
        cls.filename = LOGS_DIR+r"\\"+do_config("file_path", "log_path")
        cls.file = open(cls.filename, mode="a", encoding="utf-8")
        do_log.info("{}".format("开始执行充值功能用例"))
        cls.do_mysql = HandleMysql()
        cls.do_request = HttpRequest()

    @classmethod
    def tearDownClass(cls) -> None:
        do_log.info("{}".format("充值功能用例执行结束"))
        cls.do_mysql.close()
        cls.do_request.close()

    @data(*case_list)
    def test_recharge(self, data_namedtuple):
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")
        case_id = data_namedtuple.case_id+1
        title = data_namedtuple.title
        new_data = json.loads(HandleParameter.recharge_parameter(data_namedtuple.data))
        check_sql = data_namedtuple.check_sql
        if check_sql:
            leaveAmount_before_recharge = TestRecharge.do_mysql(check_sql, args=(new_data["mobilephone"], ))

        response = TestRecharge.do_request(method=data_namedtuple.method,
                                           url=do_config("api", "prefix_url")+data_namedtuple.url,
                                           data=new_data)
        actual = json.loads(response.text)
        actual["data"] = None

        try:
            self.assertEqual(200, response.status_code, msg="测试【{}】时，请求失败，状态码为【{}】".
                             format(title, response.status_code))
        except AssertionError as e:
            do_log.error("具体异常信息为：".format(e))
            raise e

        try:
            self.assertEqual(json.loads(data_namedtuple.expected),
                             actual,
                             msg="测试【{}】失败".format(title))
            if check_sql:
                leaveAmount_after_recharge = TestRecharge.do_mysql(check_sql, args=(new_data["mobilephone"],))
                actual_amount = leaveAmount_after_recharge["LeaveAmount"] - leaveAmount_before_recharge["LeaveAmount"]
                self.assertEqual(float(new_data["amount"]),
                                 round(float(actual_amount)),
                                 msg="充值金额有误")

        except AssertionError as e:
            do_log.error("{}，测试结果为：{}\n，具体异常信息为{}".format(title, run_fail_msg, e))
            self.parser_excel.write_result_to_excel(row=case_id, actual=response.text, result=run_fail_msg)
            raise e
        else:
            do_log.info("{},测试结果为：{}".format(title, run_success_msg))
            self.parser_excel.write_result_to_excel(row=case_id, actual=response.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()

# {"status":1,"code":"10001","data":
#     {"id":115,"regname":"小蜜蜂","pwd":"E10ADC3949BA59ABBE56E057F20F883E","mobilephone":"15138721460",
#      "leaveamount":"2000.00","type":"1","regtime":"2021-02-21 02:35:48.0"},"msg":"充值成功"}
