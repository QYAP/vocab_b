# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   hello_world.py
@Time    :   2020/11/30 18:07:10
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here

from ..base.base_handle import BaseRequestHandle


class HelloWorldHandle(BaseRequestHandle):
    async def get(self, *args, **kwargs):
        self.make_response("Hello World!")
