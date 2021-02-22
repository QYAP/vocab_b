# encoding: utf-8
# Author    : AP
# Datetime  : 2019/8/21 9:36
# Project   : RBAC

from .final import FinalProperty
from .reflect import reflect_attr
from ..utils.dict_helper import get_val_by_key


class SimpleEnum(FinalProperty):

    # 不允许实例化
    def __new__(cls, values, *args, **kwargs):
        return get_val_by_key(reflect_attr(cls), values)


# from app.libs.build_in.final import FinalProperty
# from app.libs.build_in.reflect import reflect_attr
# from app.libs.utils.dict_helper import get_val_by_key
#
#
# class SimpleEnum(FinalProperty):
#
# 	# 不允许实例化
# 	def __new__(cls, values, *args, **kwargs):
# 		return get_val_by_key(reflect_attr(cls), values)
# class Test(SimpleEnum):
# 	a=1
# 	b=2
# print(Test.a)
# print(Test(1))
