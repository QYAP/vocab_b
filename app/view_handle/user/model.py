# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   user.py
@Time    :   2020/12/03 16:29:41
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here

from ...base.base_model import BaseModel
from peewee import CharField, BigIntegerField


class User(BaseModel):
    user_id = CharField(max_length=64, verbose_name="用户名", primary_key=True)
    nickname = CharField(max_length=30, verbose_name="昵称")
    password = CharField(max_length=64, verbose_name="用户密码")
    phone = BigIntegerField(verbose_name="手机号码", unique=True)

    class Meta:
        table_name = "user"
