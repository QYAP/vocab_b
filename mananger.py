# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   mananger.py
@Time    :   2020/11/30 14:42:21
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from tornado import ioloop
from tornado import web
import wtforms_json


from config.config import settings
from app.base import sql_db
from app.base.urlpattern import urlpattern


if __name__ == "__main__":
    # 初始化wtf插件
    import wtforms_json
    wtforms_json.init()

    app = web.Application(urlpattern)
    app.listen(settings["port"])
    app.sql_db = sql_db
    ioloop.IOLoop.current().start()
