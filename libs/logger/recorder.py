# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   recorder.py
@Time    :   2020/03/05 22:03:36
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
import os
import sys
import threading

from .level import Level


def currentframe():
    return sys._getframe(6)


# if hasattr(sys, '_getframe'):
#     currentframe = lambda: sys._getframe(6)
# else:

#     def currentframe():
#         """Return the frame object for the caller's stack frame."""
#         try:
#             raise Exception
#         except Exception:
#             return sys.exc_info()[2].tb_frame.f_back


# Start typing your code from here
class Recorder():
    '''
        args:
            message:日志信息
            level_name:日志登记名
            format:格式
            color:颜色

            lineno:代码行
            func_name:方法名
            module:模块名
            file_name:文件名
            path:文件路径
            
            thread_id:线程id
            thread_name:线程名
            process_id:进程id

    '''
    def __init__(self, msg: str, level: int, formater: str, color: int):

        self.message = msg
        self.level = level
        self.level_name = Level.get_name(self.level)
        self.formater = formater
        self.color = color

        # 获取代码位置信息
        code_location = self.get_code_location()
        self.line_no = code_location.get("line_no")
        self.func_name = code_location.get("func_name")
        self.module = code_location.get("module")
        self.file_name = code_location.get("file_name")
        self.path = code_location.get("path")

        # 获取进程线程信息
        t_attribute = threading.currentThread()
        self.thread_id = t_attribute.ident
        self.thread_name = t_attribute.getName()
        self.process_id = os.getpid()
        self.attribute_json = {
            "message": self.message,
            "level": self.level,
            "level_name": self.level_name,
            "color": self.color,
            "line_no": self.line_no,
            "func_name": self.func_name,
            "module": self.module,
            "file_name": self.file_name,
            "path": self.path
        }
        self.format_msg = self.formater % self.attribute_json
        self.attribute_json["format_msg"] = self.format_msg

    def get_code_location(self):
        f = currentframe()
        code_location = f.f_code
        return {
            "line_no": f.f_lineno,
            "func_name": code_location.co_name,
            "module": code_location.co_name,
            "file_name": code_location.co_filename,
            "path": code_location.co_filename
        }

    def json(self):
        return self.attribute_json
