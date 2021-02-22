# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   base_handle.py
@Time    :   2020/11/30 18:09:35
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
import json
from typing import Iterable
from tornado.web import RequestHandler

from libs.flasker.data_filter import data_filter


class BaseRequestHandle(RequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.args = {}

    def prepare(self):
        """
        docstring
        """

        # 处理url query和form参数
        self.args.update(self.request.arguments)
        # self.args.update(self.request.query_arguments)
        # self.args.update(self.request.body_arguments)

        # 处理单一参数数组化问题
        for k, v in self.args.items():
            if len(v) == 1:
                self.args[k] = v[0].decode("utf-8")

        # 处理json
        if self.request.headers.get("Content-Type", None) and "application/json" in self.request.headers.get("Content-Type", None):
            self.args.update(json.loads(self.request.body.decode("utf-8")))


    def make_response(self, data=None, code: int = 200, msg: str = "success"):
        resp = {}
        resp["code"] = code
        if isinstance(msg, str):
            resp["msg"] = msg
        elif isinstance(msg, dict):
            resp["msg"] = ""
            for i, content in enumerate(msg.values()):
                if i > 0:
                    resp["msg"] += " | "
                resp["msg"] += str(content)
        elif isinstance(msg, list):
            resp["msg"] = ""
            for i, content in enumerate(msg):
                if i > 0:
                    resp["msg"] += " | "
                resp["msg"] += str(content)
        else:
            resp["msg"] = str(msg)

        resp["data"] = data_filter(data)
        self.finish(resp)

    def set_default_headers(self) -> None:
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass
