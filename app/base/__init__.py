# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   __init__.py
@Time    :   2020/12/03 16:29:30
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here

import peewee_async
from peewee_async import Manager
from config.config import sql_db_settings

database = peewee_async.MySQLDatabase(
    sql_db_settings["name"],
    host=sql_db_settings["host"],
    port=sql_db_settings["port"],
    user=sql_db_settings["user"],
    password=sql_db_settings["password"]
)
sql_db = Manager(database)
database.set_allow_sync(False)
