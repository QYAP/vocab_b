# -*- coding: utf-8 -*-
# @Time    : 2020/5/25 15:44
# @Author  : AP
# @File    : hook.py
# @Software: PyCharm
from functools import wraps
from . import Factory


def log_file_hook(path, color_or_not=True):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            import builtins
            ori_print = builtins.print
            hook_file_logger = Factory().quick_file_logger(path=path, color_or_not=color_or_not)
            builtins.print = hook_file_logger.auto_info
            res = func(*args, **kwargs)
            builtins.print = ori_print
            return res

        return inner

    return wrapper
