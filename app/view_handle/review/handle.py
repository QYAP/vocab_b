# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   handle.py
@Time    :   2021/01/16 16:19:34
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import time,datetime
from playhouse.shortcuts import model_to_dict
from .form import *
from .model import *
from ..vocab_book.model import *
from ..vocab_word.model import *
from ...base.base_handle import BaseRequestHandle
from libs.utils.hash_helper import sha256


class ReviewHandle(BaseRequestHandle):
    async def get(self):
        review_record_form = ReviewRecordForm.from_json(self.args)
        if review_record_form.validate():
            vocab_book_rec = await self.application.sql_db.get(
                VocabBook,
                vocab_book_id=review_record_form.vocab_book_id.data
            )
            reviewed_num = await self.application.sql_db.count(
                ReviewRecord.select().where(
                    ReviewRecord.vocab_book_id == review_record_form.vocab_book_id.data,
                    ReviewRecord.created_timestamp >= int(time.mktime(datetime.date.today().timetuple())*1000),
                    ReviewRecord.created_timestamp <= int(time.mktime(datetime.date.today().timetuple())*1000 + 24*60*60*1000),

                )
            )
            recs = await self.application.sql_db.execute(
                VocabWord.select().join(ReviewRecord, join_type="LEFT JOIN", on=(VocabWord.vocab_word_id == ReviewRecord.vocab_word_id)).where(
                    ReviewRecord.vocab_word_id == None
                ).limit(vocab_book_rec.daily_plan_pass_word-reviewed_num)
            )
            res = []
            for i in recs:
                res.append(model_to_dict(i))
            self.make_response(data={"total_num": len(res), "list": res})

    async def post(self):
        review_record_form = ReviewRecordForm.from_json(self.args)
        if review_record_form.validate():
            review_id = sha256(
                str(time.time()) + review_record_form.vocab_book_id.data + review_record_form.vocab_word_id.data)
            try:
                await self.application.sql_db.create(
                    ReviewRecord,
                    review_id=review_id,
                    vocab_book_id=review_record_form.vocab_book_id.data,
                    vocab_word_id=review_record_form.vocab_word_id.data,
                    pass_or_not=review_record_form.pass_or_not.data
                )
                self.make_response()
            except Exception as e:
                self.make_response(code=500, msg=str(e))
        else:
            self.make_response(code=400, msg=review_record_form.errors)
