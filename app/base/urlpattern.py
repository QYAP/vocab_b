# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   urlpattern.py
@Time    :   2020/12/07 13:41:51
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from tornado.web import url
from ..view_handle.hello_world import HelloWorldHandle
from ..view_handle.user.urlpattern import urlpattern as user_url
from ..view_handle.vocab_book.urlpattern import urlpattern as vocab_book_url
from ..view_handle.vocab_word.urlpattern import urlpattern as vocab_word_url
from ..view_handle.review.urpattern import urlpattern as review_record_url
urlpattern = [(url("/hello-world/?", HelloWorldHandle))]
urlpattern += user_url
urlpattern += vocab_book_url
urlpattern += vocab_word_url
urlpattern += review_record_url
