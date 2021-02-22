# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   singleton.py
@Time    :   2020/03/01 17:52:25
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''

# Start typing your code from here


# 实现单例模式
def singleton(*args, **kwargs):
    def inner(cls):
        instance = cls(*args, **kwargs)
        cls.__call__ = lambda self: instance
        return instance

    return inner


if __name__ == "__main__":

    @singleton(a=1)
    class Test():
        def __init__(self, a) -> None:
            self.a = a

    print(Test.a)
