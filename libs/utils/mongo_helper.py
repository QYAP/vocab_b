# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   mongo_helper.py
@Time    :   2020/04/10 10:51:01
@Author  :   AP 
@Version :   0.0.3
'''
# Start typing your code from here

import pymongo
from pymongo.errors import BulkWriteError
from pymongo.collection import Collection

from libs.utils.time_helper import get_date, get_datetime, get_timestamp


def get_collection(url: str, db_name: str, col_name: str, connect: bool = False) -> Collection:
    return pymongo.MongoClient(url, connect=connect).get_database(db_name).get_collection(col_name)


def dumpe_mongo(docs: dict or list, url: str, db_name: str, col_name: str):
    if isinstance(docs, dict):
        docs = [docs]
    # 处理时间
    for i in docs:
        if "created_date" not in i.keys():
            i.update({"created_date": get_date()})
        if "created_datetime" not in i.keys():
            i.update({"created_datetime": get_datetime()})
        if "created_timestamp" not in i.keys():
            i.update({"created_timestamp": get_timestamp()})
        if "last_updated_timestamp" not in i.keys():
            i.update({"last_updated_timestamp": get_timestamp()})
    if docs:
        col = get_collection(url, db_name, col_name)
        try:
            col.insert_many(docs, ordered=False)
        except BulkWriteError:
            pass
        except Exception as e:
            print("error:\tfunc dump_mongo error.")
            print(e)
        col.database.client.close()

#
# def dump_mongo(doc_or_docs: dict or list, COL: Collection):
#     recs = []
#     time_info = {
#         "created_date": get_date(),
#         "created_datetime": get_datetime(),
#         "created_timestamp": get_timestamp(),
#         "last_updated_timestamp": get_timestamp()
#     }
#     if isinstance(doc_or_docs, dict):
#         try:
#             if doc_or_docs:
#                 doc_or_docs.update(time_info)
#                 COL.insert_one(doc_or_docs)
#         except Exception as e:
#             print("error:\tfunc dump_mongo error.")
#             print(e)
#     elif isinstance(doc_or_docs, list):
#
#         for i in doc_or_docs:
#             if i:
#                 i.update(time_info)
#                 recs.append(i)
#         if recs:
#             try:
#                 COL.insert_many(recs, ordered=False)
#             except BulkWriteError:
#                 pass
#             except Exception as e:
#                 print("error:\tfunc dump_mongo error.")
#                 print(e)
#     else:
#         raise Exception("func dump_mongo's arg must be dict or list!!!")
#
#
# def dump_or_update_mongo(
#         doc_or_docs: dict or list,
#         filter_keys: list or tuple,
#         COL: Collection,
#         created_time_or_not: bool = False):
#     recs = []
#     if created_time_or_not:
#         time_info = {
#             "created_date": get_date(),
#             "created_datetime": get_datetime(),
#             "created_timestamp": get_timestamp(),
#             "last_updated_timestamp": get_timestamp()
#         }
#     else:
#         time_info = {
#             "last_updated_timestamp": get_timestamp()
#         }
#     if isinstance(doc_or_docs, dict):
#         try:
#             if doc_or_docs:
#                 doc_or_docs.update(time_info)
#                 COL.insert_one(doc_or_docs)
#         except:
#             pass
#     elif isinstance(doc_or_docs, list):
#
#         for i in doc_or_docs:
#             if i:
#                 i.update(time_info)
#                 recs.append(i)
#         if recs:
#             # COL.insert_many(recs, ordered=False)
#             for i in doc_or_docs:
#                 try:
#                     filter_i = {}
#                     for k in filter_keys:
#                         filter_i[k] = i[k]
#                     COL.update_one(filter_i, {"$set": i}, upsert=True)
#                 except Exception as e:
#                     print(e)
#     else:
#         raise Exception("func dump_mongo's arg must be dict or list!!!")
#
#
# def get_client(conf: dict = None, connect: bool = False) -> MongoClient:
#     # 初始化DB
#     if conf:
#         client = pymongo.MongoClient(conf["MONGO_URL"], connect=connect)
#     else:
#         client = pymongo.MongoClient(Config.MONGO_URL, connect=connect)
#     return client
#
#
# def get_cont(col_name: str, conf: dict or object = None, connect: bool = False) -> (Collection, Database, MongoClient):
#     # 初始化DB
#
#     if conf:
#         if isinstance(conf, dict):
#             client = pymongo.MongoClient(conf["MONGO_URL"], connect=connect)
#             novel_db = pymongo.MongoClient(conf["MONGO_URL"], connect=connect).get_database(conf["MONGO_DB_NAME"])
#         else:
#             client = pymongo.MongoClient(getattr(conf, "MONGO_URL"), connect=connect)
#             novel_db = pymongo.MongoClient(getattr(conf, "MONGO_URL"), connect=connect).get_database(
#                 getattr(conf, "MONGO_DB_NAME"))
#     else:
#         client = pymongo.MongoClient(Config.MONGO_URL, connect=connect)
#         novel_db = client.get_database(Config.MONGO_DB_NAME)
#     return novel_db.get_collection(col_name), novel_db, client
#
#
# def get_col(col_name: str, conf: dict or object = None, connect: bool = False) -> Collection:
#     # 初始化DB
#     if conf:
#         if isinstance(conf, dict):
#             novel_db = pymongo.MongoClient(conf["MONGO_URL"], connect=connect).get_database(conf["MONGO_DB_NAME"])
#         else:
#             novel_db = pymongo.MongoClient(getattr(conf, "MONGO_URL"), connect=connect).get_database(
#                 getattr(conf, "MONGO_DB_NAME"))
#     else:
#         novel_db = pymongo.MongoClient(Config.MONGO_URL, connect=connect).get_database(Config.MONGO_DB_NAME)
#     return novel_db.get_collection(col_name)
#
#
