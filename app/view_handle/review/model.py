# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   model.py
@Time    :   2021/01/16 16:11:18
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here

from ...base.base_model import BaseModel
from peewee import CharField, IntegerField, BooleanField


class ReviewRecord(BaseModel):
    review_id = CharField(
        max_length=64, verbose_name="复习记录ID", primary_key=True)
    vocab_book_id = CharField(max_length=64, verbose_name="单词本ID")
    vocab_word_id = CharField(max_length=64, verbose_name="单词ID")
    pass_or_not = IntegerField(default=1, verbose_name="是否通过")

    class Meta:
        table_name = "review_record"
