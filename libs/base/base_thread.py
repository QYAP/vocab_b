# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   base_thread.py
@Time    :   2020/07/16 16:02:18
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
from threading import Thread

# Start typing your code from here
class BaseThread(Thread):
    def __init__(self, *args, **kwargs):
        super(BaseThread, self).__init__()
        self._res = None

    @property
    def result(self):
        if self._res:
            return self._res
        else:
            return False

    @result.setter
    def result(self, res):
        self._res = res