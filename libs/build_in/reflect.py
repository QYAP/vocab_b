# encoding: utf-8
# Author    : AP
# Datetime  : 2019/8/21 9:44
# Project   : RBAC
from inspect import isfunction, ismethod
import re
import functools


def reflect_attr(obj: object) -> dict:
    """
	获取类或类实例的用户自定义的所有属性和方法
	:param obj: 类或类实例
	:return: {"property_name":property_value}
	"""
    attr = {}
    for item in dir(obj):
        if not (ismethod(getattr(obj, item)) or isfunction(getattr(obj, item)) or re.match("__[\s\S]*__", item)):
            attr[item] = getattr(obj, item)
    return attr


def reflect_func(obj: object) -> dict:
    """
	获取类或类实例的用户自定义的所有属性和方法
	:param obj: 类或类实例
	:return: {"func_name":func}
	"""
    funcs = {}
    for item in dir(obj):
        if (ismethod(getattr(obj, item)) or isfunction(getattr(obj, item))) and not re.match("__[\s\S]*__", item):
            funcs[item] = getattr(obj, item)
    return funcs


def class_exc_raiser(exc_raised=None):
    """
	类装饰器，为类的每个类方法和静态方法增加异常处理，并且可以被继承
	ps:该装饰器修饰的类如果带有实例方法，会报错，不适用于类得实例方法
	ps:被继承时，不支持类的属性继承
	"""
    def inner(cls):
        def safe_run(func, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if exc_raised is None:
                    print(e)
                else:
                    print(exc_raised)

        funcs = reflect_func(cls)

        for k_name, v_func in funcs.items():
            setattr(cls, k_name, functools.partial(safe_run, v_func))
        return cls

    return inner
