# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/2/19 10:50
@Author   :John
@Email    :337901080@qq.com
@File     :handle_request.py
@Software :PyCharm
********************************
"""
import json

import requests

from MyFinanceAPI.scripts.handle_log import do_log


class HttpRequest:
    """
    处理请求
    """
    def __init__(self):
        self.one_session = requests.Session()

    def __call__(self, method, url, data=None, is_json=False, **kwargs):
        method = method.lower()
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                do_log.error("将json格式数据转换为python中字典类型时，出现异常：{}".format(e))
                data = eval(data)

        if method == "get":
            resp = self.one_session.request(method=method, url=url, params=data, **kwargs)
        elif method == "post":
            if is_json:
                resp = self.one_session.request(method=method, url=url, json=data, **kwargs)
            else:
                resp = self.one_session.request(method=method, url=url, data=data, **kwargs)
        else:
            do_log.error("不支持【{}】请求方法".format(method))
            resp = None
        return resp

    def close(self):
        self.one_session.close()


do_request = HttpRequest()

if __name__ == '__main__':
    # 构造url
    register_url = "http://192.168.65.129:8888/futureloan/mvc/api/member/register"
    login_url = "http://192.168.65.129:8888/futureloan/mvc/api/member/login"
    recharge_url = "http://192.168.65.129:8888/futureloan/mvc/api/member/recharge"
    # 构造请求参数
    register_params = {"mobilephone": "15556075395", "pwd": "Gl123456"}
    login_params = {"mobilephone": "15556075396", "pwd": "Gl123456"}
    recharge_params = {"mobilephone": "15556075395", "amount": 1000}

    http_request = HttpRequest()
    resp_01 = http_request("post", login_url, data=login_params)
    print(resp_01.text)
    http_request.close()

