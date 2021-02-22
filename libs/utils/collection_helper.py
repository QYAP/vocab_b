# encoding: utf-8
# Author    : AP
# Datetime  : 2019/8/21 11:03
# Project   : RBAC


def page_list(target_l: list, page: int, size: int):
    num = len(target_l)
    offset = (page - 1) * size

    return num, target_l[offset:offset + size]




if __name__ == "__main__":
    t = [1, 2, 3, 4, 5, 6, 7]
    print(page_list(t, 3, 3))
