# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   handle.py
@Time    :   2020/12/15 22:39:19
@Author  :   AP
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import time
from playhouse.shortcuts import model_to_dict
from ...base.base_handle import BaseRequestHandle
from .form import *
from .model import *
from libs.utils.hash_helper import sha256


class VocabBookHandle(BaseRequestHandle):
    async def post(self):
        vocab_book_form = VocabBookForm.from_json(self.args)
        if vocab_book_form.validate():
            vocab_book_id = sha256(
                str(time.time()) + vocab_book_form.vocab_book_name.data + vocab_book_form.user_id.data)
            try:
                await self.application.sql_db.create(
                    VocabBook,
                    user_id=vocab_book_form.user_id.data,
                    vocab_book_id=vocab_book_id,
                    vocab_book_name=vocab_book_form.vocab_book_name.data,
                    position=vocab_book_form.position.data,
                    desc=vocab_book_form.desc.data,
                    cover=vocab_book_form.cover.data,
                    daily_plan_pass_word=vocab_book_form.daily_plan_pass_word.data,
                    remind_or_not=vocab_book_form.remind_or_not.data
                )
                self.make_response()
            except Exception as e:
                self.make_response(code=500, msg=str(e))
        else:
            self.make_response(code=400, msg=vocab_book_form.errors)

    async def get(self):
        vocab_book_form = VocabBookForm.from_json(self.args)
        if vocab_book_form.validate():
            total_num = await self.application.sql_db.count(
                VocabBook.select().where(
                    VocabBook.user_id == vocab_book_form.user_id.data
                )
            )
            recs = await self.application.sql_db.execute(
                VocabBook.select().where(
                    VocabBook.user_id == vocab_book_form.user_id.data
                ).paginate(vocab_book_form.page.data, vocab_book_form.size.data)
            )
            res = []
            for i in recs:
                vocab_i = model_to_dict(i)
                vocab_i["daily_remind_time"] = "06:30"
                vocab_i["plan_finish_date"] = "2021-03-10"
                vocab_i["total_word_num"] = "384"
                vocab_i["learned_word_num"] = "17"
                res.append(vocab_i)
            self.make_response(data={"total_num": total_num, "list": res})
        else:
            self.make_response(code=400, msg=vocab_book_form.errors)

    async def put(self):
        pass

    async def delete(self):
        vocab_book_form = VocabBookForm.from_json(self.args)
        if vocab_book_form.validate():
            try:
                await self.application.sql_db.execute(
                    VocabBook.delete().where(VocabBook.user_id == vocab_book_form.user_id.data,
                                     VocabBook.vocab_book_id == vocab_book_form.vocab_book_id.data)
                )
                self.make_response()
            except Exception as e:
                self.make_response(code=500, msg=str(e))
        else:
            self.make_response(code=400, msg=vocab_book_form.errors)
