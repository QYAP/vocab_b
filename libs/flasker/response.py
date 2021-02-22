# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   response.py
@Time    :   2020/04/09 16:21:39
@Author  :   AP 
@Version :   0.0.3
'''
# Start typing your code from here
from flask import make_response, jsonify
from .data_filter import data_filter


def get_r_json(res):
    return jsonify({"code": 200, "msg": "OK", "data": res})


def make_data_response(data: object = None,
                       msg: str = "OK",
                       code: int = 200,
                       http_code: int = 200,
                       cookies: dict = None):
    resp_data = {"code": code, "msg": msg, "data": data_filter(data)}
    resp = make_response(resp_data, http_code)
    if cookies:
        for k, v in cookies.items():
            resp.set_cookie(k, v)
    return resp


# def make_dirFileInfo_response(int_code=1, str_msg="", dirFileInfoBean=DirFileInfoBean(), int_respCode=200):
#     data = {"myCode": int_code, "myMsg": str_msg, "dirFileInfo": dirFileInfoBean.get_dict()}
#     resp = make_response(jsonify(data), int_respCode)
#     return resp
#
#
def make_file_response(file_name: str, file_bytes: bytes, int_respCode=200):
    resp = make_response(file_bytes, int_respCode)
    resp.headers['Content-Type'] = 'application/octet-stream'
    resp.headers['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        file_name.encode('utf-8').decode('ISO-8859-1'))
    return resp
