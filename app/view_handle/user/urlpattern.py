# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   urlpattern.py
@Time    :   2020/12/07 13:39:01
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from tornado.web import url
from .handle import *

urlpattern = (
    url("/user/?", UserHandle),
)
