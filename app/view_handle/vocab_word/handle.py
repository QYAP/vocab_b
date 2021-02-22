# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   handle.py
@Time    :   2020/12/15 23:55:24
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from app.view_handle.vocab_book.model import VocabBook
import time
from playhouse.shortcuts import model_to_dict
from ...base.base_handle import BaseRequestHandle
from .model import *
from .form import *
from libs.utils.hash_helper import sha256


class VocabWordHandle(BaseRequestHandle):
    async def post(self):
        vocab_word_form = VocabWordForm.from_json(self.args)
        if vocab_word_form.validate():
            vocab_word_id = sha256(
                str(time.time()) + vocab_word_form.english.data + vocab_word_form.vocab_book_id.data)
            try:
                await self.application.sql_db.create(
                    VocabWord,
                    vocab_word_id=vocab_word_id,
                    vocab_book_id=vocab_word_form.vocab_book_id.data,
                    english=vocab_word_form.english.data,
                    chinese=vocab_word_form.chinese.data
                )
                self.make_response()
            except Exception as e:
                self.make_response(code=500, msg=str(e))
        else:
            self.make_response(code=400, msg=vocab_word_form.errors)

    async def get(self):
        vocab_word_form = VocabWordForm.from_json(self.args)
        if vocab_word_form.validate():
            total_num = await self.application.sql_db.count(
                VocabWord.select().where(
                    VocabWord.vocab_book_id == vocab_word_form.vocab_book_id.data
                )
            )
            recs = await self.application.sql_db.execute(
                VocabWord.select().where(
                    VocabWord.vocab_book_id == vocab_word_form.vocab_book_id.data
                ).paginate(vocab_word_form.page.data, vocab_word_form.size.data)
            )
            res = []
            for i in recs:
                res.append(model_to_dict(i))
            self.make_response(data={"total_num": total_num, "list": res})
        else:
            self.make_response(code=400, msg=vocab_word_form.errors)

    async def put(self):
        pass

    async def delete(self):
        vocab_word_form = VocabWordForm.from_json(self.args)
        if vocab_word_form.validate():
            try:
                await self.application.sql_db.execute(
                    VocabWord.delete().where(
                        VocabWord.vocab_book_id == vocab_word_form.vocab_book_id.data,
                        VocabWord.vocab_word_id == vocab_word_form.vocab_word_id.data)
                )
                self.make_response()
            except Exception as e:
                self.make_response(code=500, msg=str(e))
        else:
            self.make_response(code=400, msg=vocab_word_form.errors)
