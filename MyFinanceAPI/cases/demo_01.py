# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/4/5 8:07
@Author   :John
@Email    :337901080@qq.com
@File     :demo_01.py
@Software :PyCharm
********************************
"""


class Demo:

    @staticmethod
    def func_01(num):
        """斐波纳契数列"""
        a, b = 0, 1
        new_list = []
        while a < num:
            new_list.append(a)
            a, b = b, a+b
        return new_list[-1]


if __name__ == '__main__':
    obj = Demo()
    print(isinstance(obj, Demo))
    print(obj.func_01(10))