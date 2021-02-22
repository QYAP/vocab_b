# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   time_helper.py
@Time    :   2020/04/05 00:14:18
@Author  :   AP 
@Version :   0.0.1
'''

# Start typing your code from here
import time
import datetime


def get_timestamp() -> int:
    return int(time.time() * 1000)


def get_datetime() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_date() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_date_yesterday() -> str:
    return time.strftime('%Y-%m-%d', time.localtime((get_timestamp() - 60 * 60 * 24 * 1000) / 1000))


def get_zero_timestamp() -> int:
    return (int(time.time()) - int(time.time() - time.timezone) % 86400) * 1000


def get_timestamp_by_str(datetime_str: str, format: str = "%Y-%m-%d %H:%M:%S") -> int:
    time_array = time.strptime(datetime_str, format)
    time_stamp = time.mktime(time_array)
    return int(time_stamp * 1000)


def get_datetime_from_timestamp(timestamp_13: int) -> str:
    return datetime.datetime.fromtimestamp(int(timestamp_13 / 1000))
