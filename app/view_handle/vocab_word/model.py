# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   model.py
@Time    :   2020/12/15 23:55:27
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from ...base.base_model import BaseModel
from peewee import CharField, IntegerField, BooleanField


class VocabWord(BaseModel):
    vocab_word_id = CharField(
        max_length=64, verbose_name="单词ID", primary_key=True)
    vocab_book_id = CharField(max_length=64, verbose_name="单词本ID")
    english = CharField(max_length=100, verbose_name="英文")
    chinese = CharField(max_length=100, verbose_name="中文")

    class Meta:
        table_name = "vocab_word"
