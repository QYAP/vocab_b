# encoding: utf-8
# Author    : AP
# Datetime  : 2019/7/31 10:47
# Project   : RBAC
class FinalClassProperty(type):
    """
	通过元类继承，赋予类属性不可修改特性
	"""
    def __init__(self, *args, **kwargs):
        super(FinalClassProperty, self).__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if name in self.__dict__ or name in dir(self):
            pass
        else:
            super().__setattr__(name, value)


class FinalProperty(metaclass=FinalClassProperty):
    """
	通过继承，赋予类和实例属性不可修改特性
	"""
    def __init__(self, *args, **kwargs):
        super(FinalProperty, self).__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if name in self.__dict__ or name in dir(self):
            pass
        else:
            super().__setattr__(name, value)
