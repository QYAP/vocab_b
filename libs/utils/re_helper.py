# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   re_helper.py
@Time    :   2020/07/07 18:35:24
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import re


def parse_mysql_url(url: str):
    '''
    parse msyql-url to dict
    :url: str e.g:"mysql://root:123456@127.0.0.1:3306/test?charset=utf-8"
    :returns: dict e.g:{'user': 'root', 'pwd': '123456', 'host': '127.0.0.1', 'port': '3306', 'db': 'test'}
    :raises Exception: mysql-url format error!
    '''
    res = re.findall("mysql://([\S]*):([\S]*)@([\S]*):([\d]*)/([\S]*)\?", url)
    try:
        if res:
            attrs = res[0]
            return {
                "user": attrs[0],
                "pwd": attrs[1],
                "host": attrs[2],
                "port": attrs[3],
                "db": attrs[4]
            }
        else:
            raise Exception
    except:
        raise Exception("mysql-url format error!")

if __name__ == "__main__":
    print(parse_mysql_url("mysql://root:123456@127.0.0.1:3306/test?charset=utf-8"))
