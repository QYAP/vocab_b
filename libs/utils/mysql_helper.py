# -*- coding: utf-8 -*-
# @Time    : 2020/5/28 15:19
# @Author  : AP
# @File    : mysql_helper.py
# @Software: PyCharm
from libs.base.base_sql_client import SQLClient
from libs.utils.time_helper import get_date, get_timestamp


def dumpe_mysql(datas: dict or list,
                sql_command: str,
                db_url: str,
                immediate=False):
    # 转成list
    if isinstance(datas, dict):
        datas = [datas]
    # 处理时间
    for i in datas:
        if "pt" not in i.keys():
            i.update({"pt": get_date()})
        if "tm" not in i.keys():
            i.update({"tm": get_timestamp()})
    db = SQLClient(url=db_url, max_overflow=1)
    db.execute(sql_command, datas, immediate=immediate)
    db.close()
