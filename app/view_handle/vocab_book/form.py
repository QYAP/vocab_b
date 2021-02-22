# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   form.py
@Time    :   2020/12/15 22:40:58
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from wtforms_tornado import Form
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class VocabBookForm(Form):
    vocab_book_id = StringField("单词本ID")
    user_id = StringField("用户ID", validators=[DataRequired(message="用户ID缺失")])
    vocab_book_name = StringField("单词本姓名")
    position = IntegerField("单词本位序")
    desc = StringField("单词本描述", default="")
    cover = StringField("单词本封面链接", default="")
    daily_plan_pass_word = IntegerField("单词本每日复习数", default=0)
    remind_or_not = BooleanField("是否提醒", default=False)
    page = IntegerField("页数", default=1)
    size = IntegerField("单页容量", default=10)

