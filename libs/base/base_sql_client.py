# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 1:55
# @File    : __init__.py.py
# @Software: PyCharm

import re
from copy import deepcopy
import warnings

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils.functions.database import database_exists, create_database

from contextlib import contextmanager

from libs.utils.re_helper import parse_mysql_url


class SQLClient():
    # TODO or 情况需要补充
    # TODO 将sql_maker方法都改成classmethod
    # 所有的sql片段都保证留有前置空格，后置空格需要
    def __init__(self,
                 url: str,
                 sql_create: str = "",
                 pool_size: int = 5,
                 max_overflow: int = 3,
                 pool_recycle: int = 60 * 60 * 4,
                 echo: bool = False,
                 *args,
                 **kwargs):
        self.echo = echo
        self.ATTRS = parse_mysql_url(url)

        self.ENGINE = create_engine(url,
                                    pool_size=pool_size,
                                    max_overflow=max_overflow,
                                    pool_recycle=pool_recycle,
                                    echo=False,
                                    *args,
                                    **kwargs)
        # 创建数据库
        if not database_exists(self.ENGINE.url):  #=> False
            create_database(self.ENGINE.url)

        self.SESSION = scoped_session(sessionmaker(bind=self.ENGINE))
        self.session.execute(sql_create)
        # self.session = self.Session()
        # self.connect = self.engine.connect()

    @property
    def session(self):
        return self.SESSION()

    def close(self):
        '''
        close db connect
        '''
        self.ENGINE.dispose()

    def get_col_info(self, table_name: str) -> tuple:
        sql = """
        SELECT column_name,column_comment,data_type FROM information_schema.columns 
        WHERE table_name='%s' and table_schema='%s'
        ORDER BY ORDINAL_POSITION
        """ % (table_name, self.ATTRS["db"])
        recs = self.execute(sql)
        cols_en = []
        cols_type = []
        cols_cn = []
        for i in recs:
            cols_en.append(i[0])
            cols_cn.append(i[1])
            cols_type.append(i[2])
        return cols_en, cols_cn, cols_type

    def sql_maker_insert(self,
                         table_name: str,
                         projection: dict = None,
                         cols: list = None):
        sql_insert = "INSERT INTO {} VALUES %s".format(table_name)
        cols, _, types = self.get_col_info(table_name)
        # TODO projection待完善
        these_cols = deepcopy(cols)
        these_types = deepcopy(types)
        if projection:
            for del_i, flag in projection.items():
                if flag < 0:
                    try:
                        del_index = these_cols.index(del_i)
                        these_cols.pop(del_index)
                        these_types.pop(del_index)
                    except:
                        pass

        sql_vals = []
        for index, i in enumerate(these_types):
            # todo 完善文本类型
            if i == "varchar" or i == "char" or i == "datetime":
                sql_vals.append("'{%s}'" % these_cols[index])
            else:
                sql_vals.append("{%s}" % these_cols[index])
        # 嵌入参数
        sql_insert = sql_insert % str(tuple(sql_vals))

        # 处理字符串符号'问题
        sql_insert = re.sub("'", "", sql_insert)

        # 处理单个元素tuple(*,)逗号问题
        sql_insert = re.sub(r",\)", ")", sql_insert)

        return sql_insert

    def sql_maker_del(self, table_name: str, filter: dict = None):
        sql_del = "DELETE FROM %s" % table_name
        sql_filter = self.sql_maker_where(filter=filter)
        return sql_del + sql_filter

    def sql_maker_select(self,
                         table_name: str,
                         projection: dict = None,
                         cols: list = None) -> str:
        sql_select = "SELECT * FROM %s" % table_name
        these_col = []
        if not cols:
            cols, _, _ = self.get_col_info(table_name)
        if projection:
            type_num = 0
            for _, v in projection.items():
                if isinstance(v, int):
                    type_num += v
                elif v:
                    type_num += 1
                else:
                    type_num += -1
            if abs(type_num) == len(projection):
                if type_num > 0:
                    for col_i in projection.keys():
                        # if col_i in cols:
                        these_col.append(col_i)

                else:
                    these_col = deepcopy(cols)
                    for col_i in projection.keys():
                        try:
                            these_col.remove(col_i)
                        except:
                            pass

            else:
                for col_i, v in projection.items():
                    # if v and col_i in cols:
                    these_col.append(col_i)
        else:
            these_col = deepcopy(cols)
        for index, i in enumerate(these_col):
            "TODO 待完善"
            if "count(" in i:
                these_col[index] = i
            else:
                these_col[index] = "`{}`".format(i)

        col_str = re.sub(r"[\"|']", "", re.sub(r"[\[|\]]", "", str(these_col)))
        sql_select = re.sub(r"\*", col_str, sql_select)

        return sql_select

    @classmethod
    def sql_maker_where(cls,
                        filter: dict = None,
                        range: dict = None,
                        fuzzy_search: dict = None) -> str:
        sql_where = ""

        # 判断是否加where
        if filter or fuzzy_search or range:
            sql_where += " WHERE "

        where_count = 0  # 用于判断是否需要加WHERE层用不用加AND

        # 处理filter
        if filter:
            filter_sql = ""
            filter_counter = 0  # 用于判断是否需要加filter层(=/in)用不用加AND
            for column, v in filter.items():
                if isinstance(v, dict):
                    # 处理字典操作符
                    for v_operator, v_value in v.items():
                        if filter_counter > 0:
                            filter_sql += " AND "
                        if isinstance(v_value, str):
                            filter_sql += column + " " + v_operator + " '%s'" % str(
                                v_value)
                        else:
                            filter_sql += column + " " + v_operator + " " + str(
                                v_value)
                        filter_counter += 1
                elif isinstance(v, list):
                    if len(v) > 0:
                        if filter_counter > 0:
                            filter_sql += " AND "
                        # TODO 检查[a]的情况
                        filter_sql += column + " IN " + \
                            str(v).replace("[", "(").replace("]", ")")
                    else:
                        continue
                else:
                    if filter_counter > 0:
                        filter_sql += " AND "
                    # 判断是否需要加""
                    if isinstance(v, str):
                        filter_sql += column + " = '%s'" % str(v)
                    else:
                        filter_sql += column + " = " + str(v)

                filter_counter += 1
            if len(filter_sql) > 0:
                if where_count > 0:
                    filter_sql = " AND " + filter_sql
                where_count += 1
            sql_where += filter_sql
        # 处理模糊搜索
        if fuzzy_search:
            if where_count > 0:
                fuzzy_search_sql = " AND "
            else:
                fuzzy_search_sql = ""
            where_count += 1
            fuzzy_search_counter = 0
            for k, v in fuzzy_search.items():
                if fuzzy_search_counter > 0:
                    fuzzy_search_sql += " AND "

                fuzzy_search_sql += k + " LIKE " + \
                    "'%{keyword}%'".format(keyword=v)
                fuzzy_search_counter += 1
            sql_where += fuzzy_search_sql

        # 处理范围
        if range:
            if where_count > 0:
                range_sql = " AND "
            else:
                range_sql = ""
            where_count += 1
            range_counter = 0
            for k, v in range.items():
                if range_counter > 0:
                    range_sql += " AND "
                if isinstance(v[0], int) and isinstance(v[1], int):
                    range_sql += k + " BETWEEN " + \
                        "{begin} AND {end}".format(begin=v[0], end=v[1])
                else:
                    range_sql += k + " BETWEEN " + \
                        "'{begin}' AND '{end}'".format(begin=v[0], end=v[1])
                range_counter += 1
            sql_where += range_sql
        return sql_where

    def sql_maker_order(self, sort: dict = None) -> str:
        sql_order = ""

        if sort:
            sort_sql = " ORDER BY "
            sort_counter = 0
            for k, v in sort.items():
                if sort_counter > 0:
                    sort_sql += " , "
                sort_sql += k + " " + ('ASC' if v > 0 else 'DESC')
                sort_counter += 1
            sql_order += sort_sql
        return sql_order

    def sql_maker_page(self, page: int, size: int) -> str:
        sql_page = ""
        if page > 0 and size > 0:
            sql_page = " limit %d,%d" % ((page - 1) * size, size)
        return sql_page

    def sql_maker_count(self, table_name: str, col_name: str = None):
        if col_name:
            return "SELECT count(%s) FROM %s" % (col_name, table_name)
        else:
            return "SELECT count(*) FROM %s" % table_name

    def sql_maker_group(self, col_name: str) -> str:
        return " GROUP BY %s" % col_name

    @classmethod
    def sql_maker_update(cls, table_name: str, setter: dict, filter: dict):
        sql_update = "UPDATE %s SET" % table_name
        counter = 0
        for k, v in setter.items():
            if counter > 0:
                sql_update += " ,"
            if isinstance(v, str):
                sql_update += (" " + k + " = '%s'") % v
            else:
                sql_update += " " + k + " = " + str(v)
            counter += 1
        sql_update += cls.sql_maker_where(filter=filter)
        return sql_update

    @staticmethod
    def get_col_ens_from_sql_select(sql_select):
        col_ens = re.findall(r"SELECT ([\S\s]*) FROM",
                             sql_select)[0].strip().split(",")
        for index, i in enumerate(col_ens):
            col_ens[index] = i.strip().replace("`", "")
        return col_ens

    def execute(self,
                sql: str,
                args=None,
                immediate=False,
                cursor_or_not=False,
                rollback=True):
        '''
        执行sql语句，自动区分查询和和CUD操作
        :sql: str sql语句
        :args: dict or list sql语句的参数，list为批插入操作参数类型
        :immediate: bool 是否批量操作
        :cursor_or_not: bool 是否返回游标，否则返回数组
        :rollback: bool 异常是否回滚
        :returns: cursor or list or None  
        '''

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sql = sql.strip()
            if not args:
                args = {}

            # 查询
            if re.search("^SELECT", sql.upper()):
                # if "SELECT" in sql.upper():
                try:
                    cursor = self.session.execute(sql.format(**args))
                    if self.echo:
                        print(sql.format(**args))
                    if cursor_or_not:
                        return cursor
                    else:
                        return cursor.fetchall()
                except Exception as e:
                    raise e
                finally:
                    self.session.close()
            # 其他操作
            else:
                if not isinstance(args, list):
                    try:
                        self.session.execute(sql.format(**args))
                        if self.echo:
                            print(sql.format(**args))
                        self.session.commit()
                    except Exception as e:
                        print(e)
                    finally:
                        self.session.close()
                # 批插入
                else:
                    if immediate:
                        for i in args:

                            if self.echo:
                                print(sql.format(**i))
                            try:

                                self.session.execute(sql.format(**i))
                                self.session.commit()
                            except Exception as e:
                                print(e)
                                if rollback:
                                    self.session.rollback()

                        self.session.close()
                    else:
                        for i in args:
                            if self.echo:
                                print(sql.format(**i))
                            try:
                                self.session.execute(sql.format(**i))
                            except Exception as e:
                                print(e)
                        try:
                            self.session.commit()
                        except Exception as e:
                            print(e)
                            if rollback:
                                self.session.rollback()

                        finally:
                            self.session.close()

    @contextmanager
    def auto_commit(self):
        '''
        自动commit上下文
        '''
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    # def merge_all(self, instances: list):
    #     for i in instances:
    #         self.session.merge(i)

    # def merge(self, instance: object):
    #     self.session.merge(instance)


if __name__ == "__main__":

    print(
        SQLClient.sql_maker_update(table_name="test",
                                   setter={
                                       "t1": "a",
                                       "t2": 1
                                   },
                                   filter={"t3": "aa"}))
