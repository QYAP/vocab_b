# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 11:10
# @File    : __init__.py.py
# @Software: PyCharm

from .. import BaseError


class DBError(BaseError):
    CODE = 70000
    DESP = "DB ERROR"


