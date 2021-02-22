# encoding: utf-8
# Author    : AP
# Datetime  : 2019/8/21 11:03
# Project   : RBAC


def get_val_by_key(tar_d: dict, tar_key, plural=False):
    res = []
    for k, v in tar_d.items():
        if v == tar_key:
            res.append(k)
    if not plural:
        if len(res) > 0:
            res = res[0]
        else:
            res = None
    return res


def safe_pop(tar_d: dict, k: str):
    if k in tar_d.keys():
        tar_d.pop(k)


def reverser(tar_d: dict) -> dict:
    reverser_d = {}
    for k, v in tar_d.items():
        reverser_d[v] = k
    return reverser_d
