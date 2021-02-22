# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 11:19
# @File    : base_sql_model.py
# @Software: PyCharm
import time
import datetime
from copy import deepcopy
import re
from typing import Tuple
# 字段相关
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text
from sqlalchemy import UniqueConstraint, Index, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from libs.utils.time_helper import get_date, get_datetime, get_timestamp

# 创建基类
from .base_sql_client import SQLClient


class BaseSQLModel():
    INIT_OR_NOT = False

    def __init__(self, db: SQLClient, table_name: str) -> None:
        self.DB = db
        self.TABLE = table_name
        self.QUERY = "SELECT * FROM " + self.TABLE
        self.DISTINCT = "SELECT DISTINCT({field}) FROM " + self.TABLE
        self.INSERT = ""
        # self.COLUMN_SQL = "SELECT column_name,column_comment,data_type FROM information_schema.columns WHERE table_name='%s' ORDER BY ORDINAL_POSITION" % self.TABLE
        self.COLUMN_EN = []
        self.COLUMN_CN = []
        self.COLUMN_TYPE = []

    @property
    def col_map_en_cn(self):
        return dict(zip(self.COLUMN_EN, self.COLUMN_CN))

    @property
    def col_map_cn_en(self):
        return dict(zip(self.COLUMN_CN, self.COLUMN_EN))

    def init(self):
        self.COLUMN_EN, self.COLUMN_CN, self.COLUMN_TYPE = self.DB.get_col_info(
            self.TABLE)
        # 处理单个元素tuple(*,)逗号问题
        self.INSERT = self.DB.sql_maker_insert(self.TABLE)
        self.INIT_OR_NOT = True

    def close(self):
        self.DB.close()

    def insert(self, args: dict or list, projection: dict = None):
        '''
        插入数据，可同时处理批量插和单插
        :args: dict or list , 批插类型为list，单插为dict
        '''
        if not self.INIT_OR_NOT:
            self.init()
        if isinstance(args, dict):
            args = [args]

        # for i in args:
        #     if "pt" not in i.keys():
        #         i.update({"pt": get_date()})
        #     if "tm" not in i.keys():
        #         i.update({"tm": get_timestamp()})

        self.DB.execute(
            self.DB.sql_maker_insert(table_name=self.TABLE,
                                     projection=projection), args)


    def delete(self, filter: dict):
        self.DB.execute(self.DB.sql_maker_del(self.TABLE, filter))

    def update(self, filter: dict, setter: dict):
        self.DB.execute(self.DB.sql_maker_update(self.TABLE, setter, filter))

    def query(self,
              projection: dict = None,
              filter: dict = None,
              range: dict = None,
              sort: dict = None,
              fuzzy_search: dict = None,
              limit: tuple = None,
              join: str = None,
              other_operation: str = None):
        # 获取表字段名和中文content
        if not self.INIT_OR_NOT:
            self.init()
        sql_select = self.DB.sql_maker_select(self.TABLE, projection,
                                              self.COLUMN_EN)
        sql_where = self.DB.sql_maker_where(filter, range, fuzzy_search)

        sql_join = " " + join if join else ""
        sql_sort = self.DB.sql_maker_order(sort)
        sql_limit = " limit %d,%d" % limit if limit else ""
        sql_other_operation = other_operation if other_operation else ""
        sql_query = sql_select + sql_join + sql_where + sql_sort + sql_limit + sql_other_operation

        recs = self.DB.execute(sql_query)
        # 从sql中获取字段名
        col_ens = self.DB.get_col_ens_from_sql_select(sql_select)

        res = []
        for i in recs:
            res.append(dict(zip(col_ens, i)))
        return res

    def query_page(self,
                   page: int = 1,
                   size: int = 10,
                   filter: dict = None,
                   projection: dict = None,
                   fuzzy_search: dict = None,
                   range: dict = None,
                   sort: dict = None,
                   cn_en: bool = False) -> tuple:
        # 获取表字段名和中文content
        if not self.INIT_OR_NOT:
            self.init()

        sql_count = self.DB.sql_maker_count(self.TABLE)
        sql_where = self.DB.sql_maker_where(filter, range, fuzzy_search)
        sql_query_num = sql_count + sql_where
        num = self.DB.execute(sql_query_num)[0][0]  # 查总页数

        sql_select = self.DB.sql_maker_select(self.TABLE, projection,
                                              self.COLUMN_EN)
        sql_sort = self.DB.sql_maker_order(sort)
        sql_page = self.DB.sql_maker_page(page, size)
        sql_query_page = sql_select + sql_where + sql_sort + sql_page
        # 查分页记
        if num > 0:
            recs = self.DB.execute(sql_query_page)
        else:
            recs = []
        # 从sql中获取字段名
        col_ens = self.DB.get_col_ens_from_sql_select(sql_select)

        res = []
        for i in recs:
            res.append(dict(zip(col_ens, i)))
        return num, res

    def distinct(self, field: str, filter: dict = None) -> list:
        # 去除空格和空行
        query_sql = self.DISTINCT.strip()

        # 判断是否加where
        if filter:
            query_sql += " WHERE "

            filter_sql = ""
            filter_counter = 0
            for k, v in filter.items():

                if isinstance(v, list):
                    if len(v) > 0:
                        if filter_counter > 0:
                            filter_sql += " AND "
                        filter_sql += k + " IN " + \
                            str(v).replace("[", "(").replace("]", ")")
                    else:
                        continue
                else:
                    if filter_counter > 0:
                        filter_sql += " AND "
                    if isinstance(v, str):
                        filter_sql += k + " = '%s'" % str(v)
                    else:
                        filter_sql += k + " = " + str(v)

                # if filter_counter > 0:
                #     filter_sql += " AND "

                filter_counter += 1
            query_sql += filter_sql

        recs = self.DB.execute(query_sql, args={"field": field})

        res = []
        for i in recs:
            res.append(i[0])
        return res

    def count(self, filter: dict = None, field: str = None) -> int or dict:
        projection = {}
        if field:
            projection[field] = 1
        projection["count(*)"] = 1
        sql_select = self.DB.sql_maker_select(self.TABLE,
                                              projection=projection,
                                              cols=self.COLUMN_EN)
        sql_where = self.DB.sql_maker_where(filter=filter)
        sql = sql_select + sql_where
        if field:
            sql += self.DB.sql_maker_group(field)
        recs = self.DB.execute(sql)
        if field:
            res = {}
            for i in recs:
                res[i[0]] = i[1]
        else:
            res = recs[0][0]
        return res

    # def


class AlchemyBaseModel(declarative_base()):
    __abstract__ = True

    created_date = Column(String(10))
    created_date_time = Column(String(19))
    created_timestamp = Column(Integer)
    last_updated_timestamp = Column(Integer)

    def __init__(self):
        self.created_date = get_date()
        self.created_date_time = get_datetime()
        self.last_updated_timestamp = self.created_timestamp = get_timestamp()

    def set_attrs(self, attrs_dict, id_or_not=False, id_name="id"):
        if id_or_not:
            for key, value in attrs_dict.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        else:
            for key, value in attrs_dict.items():
                if hasattr(self, key) and key != id_name:
                    setattr(self, key, value)
        return self
