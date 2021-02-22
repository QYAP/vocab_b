# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 15:49
# @File    : __init__.py.py
# @Software: PyCharm

from .. import BaseError


class ArgsError(BaseError):
    CODE = 60000
    DESP = "DB error"
