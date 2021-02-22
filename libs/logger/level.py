# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   level.py
@Time    :   2020/03/04 10:27:03
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here


class Level():

    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    FATAL = 50

    _levelToName = {NOTSET: "NOTSET", INFO: 'INFO', DEBUG: 'DEBUG', WARN: "WARN", ERROR: 'ERROR'}

    _nameToLevel = {
        'NOTSET': NOTSET,
        'DEBUG': DEBUG,
        'INFO': INFO,
        'WARN': WARN,
        'ERROR': ERROR,
        'FATAL': FATAL,
    }

    _intToName = {
        0: 'NOTSET',
        10: 'DEBUG',
        20: 'INFO',
        30: 'WARN',
        40: 'ERROR',
        50: 'FATAL',
    }

    @classmethod
    def get_name(cls, level_num: int):
        return cls._intToName.get(level_num, "NOTSET")
