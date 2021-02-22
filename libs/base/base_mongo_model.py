# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 11:26
# @File    : base.py.py
# @Software: PyCharm
from bson import ObjectId
from copy import deepcopy

from libs.utils.time_helper import get_date, get_datetime, get_timestamp


class BaseMongoDAO():
    COL = None

    @classmethod
    def insert_one(cls, rec: dict, *args, **kwargs):
        if "created_date" not in rec:
            rec["created_date"] = get_date()
        if "created_datetime" not in rec:
            rec["created_datetime"] = get_datetime()
        if "created_timestamp" not in rec:
            rec["created_timestamp"] = get_timestamp()

        return cls.COL.insert_one(rec, *args, **kwargs)

    @classmethod
    def insert_many(cls, recs: list, *args, **kwargs):
        for rec_i in recs:
            if "created_date" not in rec_i:
                rec_i["created_date"] = get_date()
            if "created_datetime" not in rec_i:
                rec_i["created_datetime"] = get_datetime()
            if "created_timestamp" not in rec_i:
                rec_i["created_timestamp"] = get_timestamp()
        return cls.COL.insert_many(recs, *args, **kwargs)

    @classmethod
    def delete_one(cls, info: dict, *args, **kwargs):
        filter = {'_id': ObjectId(info.pop('_id'))}
        return cls.COL.delete_one(filter, *args, **kwargs)

    @classmethod
    def delete_many(cls, filter: dict, *args, **kwargs):
        return cls.COL.delete_many(filter, *args, **kwargs)

    @classmethod
    def update_one(cls, info: dict, *args, **kwargs):
        filter = {'_id': ObjectId(info.pop('_id'))}
        return cls.COL.update_one(filter, {'$set': info}, *args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return cls.COL.find_one(*args, **kwargs)

    @classmethod
    def find(cls, page: int = -1, size: int = -1, sort: list = None, filter: dict = None, range: dict = None,
             fuzzy_search: dict = None, iterator_mode: bool = False, *args, **kwargs) -> tuple:
        """
        :param page: int
        :param size: int
        :param sort: int
        :param filter: dict
        :param fuzzy_search: dict
        :param iterator_mode:
        :param args:
        :param kwargs:
        :return:
        """

        # 处理过滤条件
        filter_assembly = cls.__process_fuzzy_search_cond(fuzzy_search)

        # 处理过滤
        if isinstance(filter, dict):
            filter_assembly.update(filter)
        # 处理过滤
        if isinstance(range, dict):
            for k, v in range.items():
                range[k] = {"$gte": v[0], "$lte": v[1]}
            filter_assembly.update(range)

        # 获取记录总数
        num = cls.COL.find(filter_assembly, *args, **kwargs).count()
        # num = cls.COL.find(filter_assembly, *args, **kwargs).hint([("$natural", 1)]).count()
        page_num = 1

        # 分页
        skip = (page - 1) * size
        # 处理不分页
        if page < 0 or size < 0:
            recs = cls.COL.find(filter_assembly, sort=sort, *args, **kwargs)
        else:
            recs = cls.COL.find(filter_assembly, sort=sort, skip=skip, limit=size, *args, **kwargs)
            page_num = int(num / size) + (1 if num % size > 0 else 0)

        if not iterator_mode:
            recs = list(recs)

        return page_num, recs

    @classmethod
    def count(cls, filter: dict) -> int:
        return cls.COL.find(filter).count()

    @classmethod
    def find_options(cls, options_key: str, filter: dict = None):
        if filter is None:
            filter = {}
        return cls.COL.find(filter).distinct(options_key)

    @classmethod
    def aggregate_find(cls, group: dict, page: int = -1, size: int = -1,
                       before_projection: dict = None,
                       before_fuzzy_search: dict = None,
                       before_filter: dict = None,
                       after_projection: dict = None,
                       after_fuzzy_search: dict = None,
                       after_filter: dict = None,
                       second_group: dict = None,
                       sort: dict = None,
                       iterator_mode: bool = False):
        pipes = []
        # 处理数据
        skip = {"$skip": (page - 1) * size}
        limit = {'$limit': size}

        # 模糊搜索
        before_filter_assembly = cls.__process_fuzzy_search_cond(before_fuzzy_search)
        after_fuzzy_search = cls.__process_fuzzy_search_cond(after_fuzzy_search)

        # 处理before
        if before_projection:
            pipes.append({"$project": before_projection})
        if before_filter_assembly:
            pipes.append({"$match": before_filter_assembly})
        if before_filter:
            pipes.append({"$match": before_filter})

        # 获取聚合后总记录
        count_pipes = deepcopy(pipes)

        # count_pipes.append({"$group": {"_id": group["_id"]}})

        # todo
        if second_group:
            count_pipes.append({"$group": group})
            count_pipes.append({"$group": {"_id": second_group["_id"]}})
        else:
            count_pipes.append({"$group": {"_id": group["_id"]}})

        count_pipes.append({"$count": "total_num"})
        total_count = cls.COL.aggregate(count_pipes)
        total_count = list(total_count)
        if total_count:
            total = total_count[0]["total_num"]
        else:
            total = 0

        pipes.append({"$group": group})
        # todo
        if second_group:
            pipes.append({"$group": second_group})

        # 处理after
        if after_projection:
            pipes.append({"$project": after_projection})
        if after_fuzzy_search:
            pipes.append({"$match": after_fuzzy_search})
        if after_filter:
            pipes.append({"$project": after_filter})

        if sort:
            pipes.append({"$sort": sort})
        if page > 0 and size > 0:
            pipes.append(skip)
            pipes.append(limit)
        if after_projection:
            pipes.append(after_projection)
        # pipes.append({"$count": "page_num"})

        recs = cls.COL.aggregate(pipes, allowDiskUse=True)
        if not iterator_mode:
            recs = list(recs)

        # 计算页数
        if page < 0 or size < 0:
            page_num = 1
        else:
            page_num = int(total / size) + (1 if total % size > 0 else 0)

        return page_num, recs

    @classmethod
    def __process_fuzzy_search_cond(cls, fuzzy_search_cond: dict):
        filter_assembly = {
            "$or": [],
            "$and": []
        }
        if isinstance(fuzzy_search_cond, dict):
            if fuzzy_search_cond.get("intersect", False):
                fuzzy_search_cond.pop("intersect", None)
                for field_name, search_str in fuzzy_search_cond.items():
                    if not (isinstance(search_str, str) and isinstance(field_name, str)):
                        continue
                    filter_assembly['$and'].append({field_name: {"$regex": "[.]*" + search_str + "[.]*"}})
            else:
                fuzzy_search_cond.pop("intersect", None)
                for field_name, search_str in fuzzy_search_cond.items():
                    if not (isinstance(search_str, str) and isinstance(field_name, str)):
                        continue
                    filter_assembly['$or'].append({field_name: {"$regex": "[.]*" + search_str + "[.]*"}})
        # 收尾处理过滤条件
        if len(filter_assembly['$or']) == 0:
            filter_assembly.pop('$or')
        if len(filter_assembly['$and']) == 0:
            filter_assembly.pop('$and')
        return filter_assembly

# def pager(col: collection, filter: dict, size: int = -1, page: int = -1, projection=None, *args, **kwargs):
#     size = int(size)
#     page = int(page)
#     if not projection:
#         projection = {"_id": False}
#
#     # 分页
#     skip = (page - 1) * size
#     # 处理不分页
#     if page < 0 or size < 0:
#         recs = col.find(filter=filter, projection=projection, *args, **kwargs)
#     else:
#         recs = col.find(filter=filter, projection=projection, skip=skip, limit=size, *args, **kwargs)
#     return recs

# from contextlib import contextmanager
# from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

#
# class SQLAlchemy(_SQLAlchemy):
#     @contextmanager
#     def auto_commit(self):
#         try:
#             yield
#             self.session.commit()
#         except Exception as e:
#             DB.session.rollback()
#             # LoggerDefined.debug(e.orig.args[0])
#             raise e
#
#
# DB = SQLAlchemy()

#
# class Base(DB.Model):
#     __abstract__ = True
#
#     def set_attrs(self, attrs_dict, id_or_not=False, id_name="id"):
#         if id_or_not:
#             for key, value in attrs_dict.items():
#                 if hasattr(self, key):
#                     setattr(self, key, value)
#         else:
#             for key, value in attrs_dict.items():
#                 if hasattr(self, key) and key != id_name:
#                     setattr(self, key, value)
#         return self
