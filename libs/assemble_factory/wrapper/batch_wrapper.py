# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   batch_wrapper.py
@Time    :   2020/09/26 03:36:00
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from types import FunctionType
from copy import deepcopy

# TODO 还需要无感知*args,**kwargs，思路是手动装配成**kwargs的传参方式


def batch(*args, **kwargs) -> list:
    batch_res = []
    if point_type == "kwargs":
        tasks = deepcopy(kwargs.get(point_key))
        for i in tasks:
            kwargs.update({point_key: i})
            batch_res.append(point_func(*args, **kwargs))
    else:
        tasks = args[point_key]
        args = deepcopy(list(args))
        for i in tasks:
            args[point_key] = i
            batch_res.append(point_func(*args, **kwargs))

    return batch_res


def batch_wrapper(point_func: FunctionType, point_position: int = None, point_name: str = None) -> FunctionType:
    # if point_name:
    #     point_type = "kwargs"
    #     point_key = point_name
    # elif point_position:
    #     point_type = "args"
    #     point_key = point_position
    # else:
    #     point_type = "args"
    #     point_key = 0
    __global = {"point_func": point_func, "point_position": point_position,
                "point_name": point_name, "deepcopy": deepcopy}
    return FunctionType(batch.__code__, __global)


if __name__ == "__main__":
    def test_a(task: int):
        return task + 1

    def test_b(task: int):
        return task + 2

    t1 = batch_wrapper(test_a, point_name="task")
    t2 = batch_wrapper(test_b, point_name="task")
    print(t2(task=[1, 2, 3]))
    print(t1(task=[1, 2, 3]))
