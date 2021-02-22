# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 0:55
# @File    : filter.py
# @Software: PyCharm
from bson import ObjectId
import datetime
from decimal import Decimal


def data_filter(data):
    def filter_list(l):
        for i, v in enumerate(l):
            if isinstance(v, dict):
                l[i] = filter_dict(v)
            elif isinstance(v, list):
                l[i] = filter_list(v)
            elif isinstance(v, ObjectId):
                l[i] = str(v)
            elif isinstance(v, datetime.datetime):
                l[i] = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, datetime.date):
                l[i] = v.strftime("%Y-%m-%d")
            elif isinstance(v, Decimal):
                l[i] = round(float(v), 2)
            elif isinstance(v, float):
                l[i] = round(v, 2)
            else:
                l[i] = v
        return l

    def filter_dict(d):
        '''
        :param d:
        :return:
        '''
        n_d = {}
        for k in d:
            v = d[k]
            if isinstance(v, ObjectId):
                n_d[k] = str(v)
            elif isinstance(v, datetime.datetime):
                n_d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, datetime.date):
                n_d[k] = v.strftime("%Y-%m-%d")
            elif isinstance(v, Decimal):
                n_d[k] = round(float(v), 2)
            elif isinstance(v, float):
                n_d[k] = round(v, 2)
            elif isinstance(v, list):
                n_d[k] = filter_list(v)
            elif isinstance(v, dict):
                n_d[k] = filter_dict(v)
            else:
                n_d[k] = v
        return n_d

    def filter_data(data):
        if isinstance(data, ObjectId):
            return str(data)
        elif isinstance(data, datetime.datetime):
            return data.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(data, datetime.date):
            return data.strftime("%Y-%m-%d")
        elif isinstance(data, Decimal):
            return round(float(data), 2)
        elif isinstance(data, float):
            return round(data, 2)
        else:
            return data

    if isinstance(data, list):
        f_data = filter_list(data)
    elif isinstance(data, dict):
        f_data = filter_dict(data)
    else:
        f_data = filter_data(data)
    return f_data
