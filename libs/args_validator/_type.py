# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   type.py
@Time    :   2020/03/01 09:54:08
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here

# 基本v值类型 int,float,complex,Number(数，包括整型和浮点型),str,list,tupple,set,dict,bool,Enumeration（枚举）,RegEx（正则）,Operator（操作符）,
"""
    Oprator：">", "<", "==", "!=", ">=", "<=", "~$"
    其中集合运算符：<=list表示子集，<list表示真子集，~list 属于
    正则运算符："~$"
"""

from ..build_in.singleton import singleton


class BaseType():
    def __init__(self, field):
        '''
            process_flag:0表示基础类型，其他数字分别表示特定的类型
        '''
        self.process_flag = 0
        self.field = set(field)


class Type(BaseType):
    '''
        基础类型
    '''
    def __init__(self, field):
        super(Type, self).__init__([field])


@singleton()
class Number(BaseType):
    '''
        自定义数型，包括整型、浮点型和复数
    '''
    def __init__(self):
        '''
            process_flag:
                0表示python内建类型
        '''
        super().__init__([int, float, complex])


class Enumeration(BaseType):
    pass


class Operator(BaseType):
    OPERATOR = [">", "<", "==", "!=", ">=", "<=", "~", "~$"]
    pass


class RegEx(BaseType):
    pass
