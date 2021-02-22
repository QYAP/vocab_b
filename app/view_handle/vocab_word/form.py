# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   form.py
@Time    :   2020/12/15 23:55:30
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from wtforms_tornado import Form
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class VocabWordForm(Form):
    vocab_word_id = StringField("单词ID")
    vocab_book_id = StringField("单词本ID")
    english = StringField("英文")
    chinese = StringField("中文")
    page = IntegerField("页数", default=1)
    size = IntegerField("单页容量", default=10)
