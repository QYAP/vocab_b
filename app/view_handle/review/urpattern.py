# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   urpattern.py
@Time    :   2021/01/16 16:19:05
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from tornado.web import url
from .handle import *

urlpattern = (
    url("/review-record/?", ReviewHandle),
)
