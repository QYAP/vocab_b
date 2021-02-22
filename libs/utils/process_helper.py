# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 12:20
# @File    : process_helper.py
# @Software: PyCharm
import os
import psutil


def pp_exist_or_not() -> bool:
    ppid = os.getppid()
    pl = psutil.pids()
    if ppid in pl:
        return True
    else:
        return False


if __name__ == '__main__':
    print(os.getppid())
    print(os.getpid())
    print(psutil.pids())
