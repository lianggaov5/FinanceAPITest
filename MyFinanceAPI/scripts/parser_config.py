# -*- coding: utf-8 -*-
"""
********************************
@Time     :2021/1/26 18:30
@Author   :John
@Email    :337901080@qq.com
@File     :parser_config.py
@Software :PyCharm
********************************
"""

from configparser import ConfigParser
from MyFinanceAPI.scripts.constants import CONFIGS_FILE_PATH


class ParserConfig(ConfigParser):
    """
    对配置文件进行封装
    """

    def __init__(self, filename):
        super().__init__()  # 重写或者拓展父类的构造方法，往往我们需要先调用父类的构造方法
        self.filename = filename

    def __call__(self, section="default", option=None, is_eval=False, is_bool=False):
        """
        读取数据
        :param section:区域值  初始值为default
        :param option: 选项值
        :param is_eval: 为默认参数，是否需要eval函数转换
        :param is_bool: 判断数据是否需要转换为bool类型，默认不转换
        :return: 从配置文件中解析后的数据
        """
        self.read(filenames=self.filename, encoding="utf-8")

        if option is None:
            return dict(self[section])
        # int float bool str
        if isinstance(is_bool, bool):
            if is_bool:
                return self.getboolean(section, option)
        else:
            raise ValueError("is_bool必须是布尔类型！")  # 手动抛出异常
        data = self.get(section, option)
        if data.isdigit():
            # data = self.getint(section, option)
            return int(data)
        try:
            # data = self.getfloat(section, option)
            return float(data)
        except ValueError:
            pass
        if isinstance(is_eval, bool):
            if is_eval:
                return eval(data)
        else:
            raise ValueError("is_eval必须是bool类型！")

        return data

    def write_to_config(self, datas):
        """
        写数据到配置文件
        :param datas: 嵌套字典的字典
        :return:
        """
        for key in datas:
            self[key] = datas[key]

        with open(self.filename, mode="w", encoding="utf-8") as file:
            self.write(file)


do_config = ParserConfig(CONFIGS_FILE_PATH)


if __name__ == '__main__':
    temp_data = {"name": {"a": 1, "b": 2},
                 "age": {"c": 3, "d": 4}}
    parser_config = ParserConfig(CONFIGS_FILE_PATH)

    temp_a = parser_config()
    temp_b = parser_config("file_path")
    a = (parser_config("file_path", "case_path"))
    # b = (parser_config("excel", "test", is_bool=True))
    # c = (parser_config("excel", "actual_col"))
    # d = (parser_config("excel", "new_dict", is_eval=True))
    # e = (parser_config("excel", "new_list", is_eval=True))
    # f = (parser_config("excel", "new_float"))

    # parser_config.write_to_config(temp_data)
    # print(parser_config.config.getfloat("excel", "new_dict")) # ValueError

    pass



