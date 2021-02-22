# # coding=utf-8
#
# """
#     Created by CHAINBASE.AI on 2019/03/04
#     Updated by CHAINBASE.AI on 2018/03/04
# """
# __author__ = "CHAINBASE.AI"
#
# from main.lib.util.dict_util import union_dict
# import requests, json
#
#
# class BaseProxy:
#     """微服务基础对象
#     """
#     url_prefix = None
#     data_header = None
#     route = {}
#
#     @classmethod
#     def check_online_or_not(cls, postfix: str):
#         """检查微服务是否正常在线
#         """
#         reqest_url = cls.url_prefix + postfix
#         if requests.get(url=reqest_url).status_code != 200:
#             return False
#         else:
#             return True
#
#     @classmethod
#     def post_json(cls, postfix: str, json_data={}, data_header=None):
#         """增加或查询请求
#         """
#         reqest_url = cls.url_prefix + postfix
#         header = {'Content-Type': 'application/json'}
#         if not data_header:
#             if cls.data_header:
#                 json_data = union_dict(cls.data_header, json_data)
#         resp = requests.post(reqest_url, headers=header, data=json.dumps(json_data))
#         return resp
#
#     @classmethod
#     def delete_json(cls, postfix: str, json_data={}, data_header=None):
#         """删除请求
#         """
#         reqest_url = cls.url_prefix + postfix
#         header = {'Content-Type': 'application/json'}
#         if not data_header:
#             if cls.data_header:
#                 json_data = union_dict(cls.data_header, json_data)
#         resp = requests.delete(reqest_url, headers=header, data=json.dumps(json_data))
#         return resp
#
#     @classmethod
#     def put_json(cls, postfix: str, json_data={}, data_header=None):
#         """更新请求
#         """
#         reqest_url = cls.url_prefix + postfix
#         header = {'Content-Type': 'application/json'}
#         if not data_header:
#             if cls.data_header:
#                 json_data = union_dict(cls.data_header, json_data)
#         resp = requests.put(reqest_url, headers=header, data=json.dumps(json_data))
#         return resp
#
#     @classmethod
#     def relay_json_post(cls, postfix: str, json_data={}, data_header=None) -> ("http_code", "json_data"):
#         """中转post请求给微服务，请求的数据只能是json
#         """
#         resp = cls.post_json(postfix, json_data, data_header)
#         return resp.status_code, resp.json()
