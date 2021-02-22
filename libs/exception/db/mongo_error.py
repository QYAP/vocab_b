# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 15:59
# @File    : mongo_error.py
# @Software: PyCharm
from . import DBError


class MongoDBError(DBError):
    CODE = 70100
    DESP = "MongoDB ERROR"


class MongoUniqueError(MongoDBError):
    CODE = 70101
    DESP = "Key duplicate!!!"
