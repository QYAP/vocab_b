# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   hash_helper.py
@Time    :   2020/09/02 17:12:27
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import hashlib


def md5(content):
    if not isinstance(content, str):
        content = str(content)
    return hashlib.md5(content.encode()).hexdigest()


def sha256(s):
    if not isinstance(s, str):
        raise Exception("arg-s is not str")
    return hashlib.sha256(s.encode()).hexdigest()
