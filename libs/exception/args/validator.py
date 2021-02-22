# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 16:00
# @File    : validator.py
# @Software: PyCharm

from . import ArgsError


class ArgsValidatorError(ArgsError):
    CODE = 60100
    DESP = "Validator error"
