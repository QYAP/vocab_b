# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   str_helper.py
@Time    :   2020/12/15 16:53:21
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from .list_helper import reverse


def leftloop_str(s, k):
    """
    字符串循环左移
    :param s: 字符串数组
    :param k: 字符串循环左移k位
    :return:
    """

    if isinstance(s, str):
        tmp = list(s)
    else:
        raise Exception("arg-s is not str")
    if tmp is None:
        return
    n = len(tmp)
    if n < k:
        return
    reverse(tmp, 0, k - 1)
    reverse(tmp, k, n - 1)
    reverse(tmp, 0, n - 1)
    return "".join(tmp)


def resver_str(s):
    if not isinstance(s, str):
        raise Exception("arg-s is not str")
    tmp = list(s)
    reverse(tmp)
    return "".join(tmp)
