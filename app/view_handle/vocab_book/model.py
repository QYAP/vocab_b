# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   model.py
@Time    :   2020/12/15 15:36:19
@Author  :   AP
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here

from ...base.base_model import BaseModel
from peewee import CharField, IntegerField, BooleanField


class VocabBook(BaseModel):
    vocab_book_id = CharField(
        max_length=64, verbose_name="单词本ID", primary_key=True)
    user_id = CharField(max_length=64, verbose_name="用户ID")
    vocab_book_name = CharField(max_length=30, verbose_name="单词本名称")
    position = IntegerField(verbose_name="单词本位序", unique=True)
    desc = CharField(max_length=300, verbose_name="单词本描述")
    cover = CharField(max_length=300, verbose_name="封面链接")
    daily_plan_pass_word = IntegerField(verbose_name="每日复习数量")
    remind_or_not = BooleanField(default=False, verbose_name="是否提醒")

    class Meta:
        table_name = "vocab_book"
