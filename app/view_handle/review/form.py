# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   form.py
@Time    :   2021/01/16 16:16:40
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from wtforms_tornado import Form
from wtforms import StringField,  BooleanField
from wtforms.validators import DataRequired


class ReviewRecordForm(Form):
    review_id = StringField("复习记录ID")
    vocab_book_id = StringField("单词本ID")
    vocab_word_id = StringField("单词ID")
    pass_or_not = BooleanField(default=False)
