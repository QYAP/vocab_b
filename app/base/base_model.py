# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   base_model.py
@Time    :   2020/12/03 17:00:32
@Author  :   AP
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import time
from peewee import Model, BigIntegerField
from . import database


class BaseModel(Model):
    created_timestamp = BigIntegerField(
        default=int(time.time()*1000), verbose_name="创建时间戳")
    last_updated_timestamp = BigIntegerField(
        default=int(time.time()*1000), verbose_name="更新时间戳")

    class Meta:
        database = database
