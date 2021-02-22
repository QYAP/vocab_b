# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   user.py
@Time    :   2020/12/01 19:41:52
@Author  :   AP
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import time
from playhouse.shortcuts import model_to_dict, dict_to_model
from ...base.base_handle import BaseRequestHandle
from .form import *
from .model import *
from libs.utils.hash_helper import sha256
from libs.utils.str_helper import resver_str, leftloop_str


class UserHandle(BaseRequestHandle):
    async def post(self):
        """
        注册用户
        """
        print(self.args)
        user_form = UserForm.from_json(self.args)

        if user_form.validate():
            phone = user_form.phone.data
            password = user_form.password.data
            password = resver_str(password)
            password = leftloop_str(password, 3)
            nickname = user_form.nickname.data
            user_id = sha256(str(time.time())+nickname)
            try:
                await self.application.sql_db.create(User, user_id=user_id, password=password, phone=phone, nickname=nickname)
                user = await self.application.sql_db.get(User.select().filter(User.phone == phone))
                self.make_response(data=model_to_dict(user))
            except Exception as e:
                self.make_response(code=500, msg=str(e))
        else:
            self.make_response(code=400, msg=user_form.errors)

    async def get(self):
        """
        登录
        """
        user_form = UserForm.from_json(self.args)
        if user_form.validate():
            phone = user_form.phone.data
            password = user_form.password.data
            password = resver_str(password)
            password = leftloop_str(password, 3)
            try:
                user = await self.application.sql_db.get(User.select().filter(User.phone == phone))
            except:
                self.make_response(code=400, msg="用户不存在")
                return

            if password == user.password:
                self.make_response(data=model_to_dict(user))
            else:
                self.make_response(code=400, msg="密码错误")

        else:
            self.make_response(code=400, msg=user_form.errors)

    async def put(self):
        user_form = UserForm.from_json(self.args)
        if user_form.validate():
            user_id = user_form.user_id.data
            password = user_form.password.data
            password = resver_str(password)
            password = leftloop_str(password, 3)
            nickname = user_form.nickname.data
            try:
                await self.application.sql_db.execute(User.update(
                    nickname=nickname, password=password).where(User.user_id == user_id))
                self.make_response()
            except:
                self.make_response(code=400)
        else:
            self.make_response(code=400, msg=user_form.errors)
