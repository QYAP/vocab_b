# encoding: utf-8
# Author    : AP
# Datetime  : 2019/7/22 16:06
# Project   : RBAC

import re

from ..build_in.singleton import singleton


@singleton()
class ConsoleColor():
    NOTSET = None
    RED = '0;31m'  # 红（用于error）
    GREEN = '0;32m'  # 绿（用于info）
    YELLOW = '0;33m'  # 黄（用于warn）

    BLUE = '0;34m'  # 蓝
    PURPLE = '0;35m'  # 紫

    GREY = '0;37m'  # 灰
    BLACK = '0;30m'  # 黑
    WHITE = '1;37m'  # 白

    LIGHT_RED = '1;31m'  # 亮红
    LIGHT_GREEN = '1;32m'  # 亮绿
    LIGHT_YELLOW = '1;33m'  # 亮绿

    LIGHT_BLUE = '1;34m'  # 亮蓝
    LIGHT_PURPLE = '1;35m'  # 亮紫

    # console颜色显示格式前后缀
    COLOR_START = '\033['
    COLOR_EDN = '\033[0m'

    def __init__(self):
        self.__nameToColor = {
            "NOTSET": self.NOTSET,
            'RED': self.RED,
            'GREEN': self.GREEN,
            'YELLOW': self.YELLOW,
            'BLUE': self.BLUE,
            'PURPLE': self.PURPLE,
            'GREY': self.GREY,
            'BLACK': self.BLACK,
            'WHITE': self.WHITE,
            'LIGHT_RED': self.LIGHT_RED,
            'LIGHT_GREEN': self.LIGHT_GREEN,
            'LIGHT_YELLOW': self.LIGHT_YELLOW,
            'LIGHT_BLUE': self.LIGHT_BLUE,
            'LIGHT_PURPLE': self.LIGHT_PURPLE
        }
        self.__colorToName = {
            self.NOTSET: "NOTSET",
            self.RED: 'RED',
            self.GREEN: 'GREEN',
            self.YELLOW: 'YELLOW',
            self.BLUE: 'BLUE',
            self.PURPLE: 'PURPLE',
            self.GREY: 'GREY',
            self.BLACK: 'BLACK',
            self.WHITE: 'WHITE',
            self.LIGHT_RED: 'LIGHT_RED',
            self.LIGHT_GREEN: 'LIGHT_GREEN',
            self.LIGHT_YELLOW: 'LIGHT_YELLOW',
            self.LIGHT_BLUE: 'LIGHT_BLUE',
            self.LIGHT_PURPLE: 'LIGHT_PURPLE'
        }

    @classmethod
    def dye(cls, target_str: str, color_type: str) -> str:
        if color_type is None:
            return target_str
        else:
            return '%s%s%s%s' % (cls.COLOR_START, color_type, target_str,
                                 cls.COLOR_EDN)

    @staticmethod
    def clean(target_str: str) -> str:
        return re.sub(r'\\033\[[\s\S]*?m{1}', '', target_str)

    def get_color(self, color: str):
        return self.__nameToColor.get(color, "NOTESET")

    def get_name(self, color_name: str):
        return self.__colorToName.get(color_name)


# print(ConsoleColor.dye("hello", ConsoleColor.BLUE))
# print(ConsoleColor.get_name(ConsoleColor.RED))
# print(ConsoleColor.get_color("RED"))
