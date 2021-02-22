# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   form.py
@Time    :   2020/12/07 13:36:16
@Author  :   AP
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class UserForm(Form):
    user_id = StringField("昵称")
    nickname = StringField("昵称", default="")
    password = StringField("密码", validators=[DataRequired(message="请输入用户密码")])
    phone = StringField("手机号码", validators=[DataRequired(message="请输入用户手机号码")])
