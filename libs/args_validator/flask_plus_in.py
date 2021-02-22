# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   flask_route_func_decorator.py
@Time    :   2020/02/28 02:38:54
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''

from functools import wraps
from flask import request

from . import Validator


# Start typing your code from here
def args_validator(rule: dict, redundant_or_not: bool = True, redundant_max_num: int = float("inf")):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            reqs_args = dict(request.values.to_dict(), **({} if request.json is None else request.json))
            Validator(
                args=reqs_args,
                rule=rule,
                redundant_or_not=redundant_or_not,
                redundant_max_num=redundant_max_num).execute()
            res = func(*args, **kwargs)
            return res

        return inner

    return wrapper
