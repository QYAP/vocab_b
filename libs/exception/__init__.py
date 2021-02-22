# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 11:09
# @File    : __init__.py.py
# @Software: PyCharm
# import sys
#
# sys.path.append("../../libs")
from inspect import getmro

from ..build_in.reflect import reflect_attr


# from libs.build_in.reflect import reflect_attr


class BaseError(Exception):
    CODE = 0

    # DESP = "BASE ERROR"

    def __init__(self, msg: str = "", *args, **kwargs):
        self.msg = msg
        super().__init__(*args, **kwargs)

    def __str__(self):
        formater = "[CODE:%(code)d]%(error_info)s%(msg)s"
        data = {"code": self.CODE, "error_info": "", "msg": " >>> %s" % self.msg if self.msg else self.msg}
        # 获取继承树并获取拼接所有字符串属性值
        for item in reversed(getmro(type(self))[0:-1]):
            attributes = reflect_attr(item)
            for k, v in attributes.items():
                if isinstance(v, str):
                    data["error_info"] += " >>> " + v
        return formater % data


class DBError(BaseError):
    CODE = 10000
    DESP = "DB ERROR"


class DuplicateError(DBError):
    CODE = 10001
    DESP = "ID duplicate!!!"

# print(DuplicateError("123"))
