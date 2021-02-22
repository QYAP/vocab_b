# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   list_helper.py
@Time    :   2020/12/15 17:00:37
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here


def reverse(s, i: int = None, j: int = None):
    """
    翻转
    :param s: 需翻转的数组
    :param i: 翻转开始位置
    :param j: 翻转结束位置
    """
    if not i and not j:
        i = 0
        j = len(s)-1
    if s is None or i < 0 or j < 0 or i >= j or len(s) < j + 1:
        return
    while i < j:
        temp = s[i]
        s[i] = s[j]
        s[j] = temp
        i += 1
        j -= 1
