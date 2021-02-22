# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   base_wrapper.py
@Time    :   2020/08/18 14:39:59
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
# !/usr/bin/python3
# encoding:utf-8
'''
@File    :   base_wrapper.py
@Time    :   2020/07/23 10:30:28
@Author  :   AP 
@Version :   1.0
@WebSite :   ***
'''
# Start typing your code from here
from copy import deepcopy
from multiprocessing.context import Process
from threading import Thread
from .base_wrapper import MultiWrapper


class ThreadWrapper(MultiWrapper, Thread):
    def __init__(self, func, crontab: str, *args, **kwargs):
        # Thread.__init__()
        super(ThreadWrapper, self).__init__(func, crontab, *args, **kwargs)
        super(ThreadWrapper, MultiWrapper).__init__()

    def run(self):
        if self._crontab:
            self._crontab_run(self._crontab, self._t_func_maker(self.func),
                              self._args, self._kwargs)
        else:
            self._t_func_maker(self.func)(*self._args, **self._kwargs).start()


class ProcessWrapper(MultiWrapper, Process):
    def __init__(self, func, crontab: str, *args, **kwargs):
        # Thread.__init__()
        super(ProcessWrapper, self).__init__(func, crontab, *args, **kwargs)
        super(ProcessWrapper, MultiWrapper).__init__()

    def run(self):
        pass

    def _concurrent_run(self, t_func, concurrent_num: int, scale: int, *args,
                        **kwargs):
        args = list(args)
        tasks = args.pop(0)
        these_tasks = []
        # 分割任务
        while len(tasks) > 0:
            these_tasks.append(tasks[:scale])
            del tasks[:scale]

        for this_task in these_tasks:
            these_threads = []
            # 生成并发处理线程
            for _ in range(concurrent_num):
                this_args = deepcopy(args)
                this_args.insert(0, this_task)
                these_threads.append(t_func(*this_args, **deepcopy(kwargs)))
            # 启动线程
            for i in these_threads:
                i.start()
            # 等待批处理接触
            for i in these_threads:
                i.join()

from copy import deepcopy
import time
from datetime import datetime

from collections import deque
from croniter import croniter
from threading import Thread

from ..logger.hook import log_file_hook


class BaseWrapper():
    def _formarter_pre_args(self, func):
        '''
        规范pre函数入参格式
        :param param1: this is a first param
        '''
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            if isinstance(res, tuple):
                if len(res) == 2 and isinstance(res[1], dict):
                    return res
                else:
                    return res, dict()
            elif isinstance(res, dict):
                return tuple(), res
            else:
                raise Exception("pre函数结果格式出错")

        return inner


class WorkerWrapper(BaseWrapper):
    def __init__(self, func):
        self._func = func
        self._pre_filters = []  # 前置过滤器
        self._pre_adaptors = []  # 前置适配器
        self._postf_filter = []  # 后置过滤器
        self._postf_adaptors = []  # 后置适配器
        # self._source = None  # 起源器
        self._dumpers = []  # 持久化器

    def add_pre_filter(self, filter):
        '''
        添加前置过滤器
        '''
        self._pre_filters.append(self._formarter_pre_args(filter))

    def add_pre_adaptor(self, adaptor):
        '''
        添加前置适配器
        '''
        self._pre_adaptors.append(self._formarter_pre_args(adaptor))

    def add_postf_filter(self, filter):
        '''
        添加后置过滤器
        '''
        self._postf_filter.append(filter)

    def add_postf_adaptor(self, adaptor):
        '''
        添加后置适配器
        '''
        self._postf_adaptors.append(adaptor)

    def add_dumper(self, dumper):
        '''
        添加持久化器
        '''
        self._dumpers.append(dumper)

    def _run_pre_filter(self, *args, **kwargs) -> tuple:
        '''
        运行前置过滤器串
        '''
        for i in self._pre_filters:
            args, kwargs = i(*args, **kwargs)
        return args, kwargs

    def _run_pre_adaptor(self, *args, **kwargs):
        '''
        运行前置适配器串
        '''
        for i in self._pre_adaptors:
            args, kwargs = i(*args, **kwargs)
        return args, kwargs

    def _run_postf_filter(self, res):
        '''
        运行后置过滤器串
        '''
        for i in self._postf_filter:
            res = i(res)
        return res

    def _run_postf_adaptor(self, res):
        '''
        运行后置适配器串
        '''
        for i in self._postf_adaptors:
            res = i(res)
        return res

    def _run_dumper(self, res):
        '''
        运行持久器组
        '''
        for i in self._dumpers:
            i(res)

    def batch(self, *args, **kwargs):
        """
        批处理函数
        """
        # todo 需要指定任务参数key名
        if not isinstance(args[0], list):
            raise Exception("Batch Eroor")

        args, kwargs = self._run_pre_filter(*args, **kwargs)
        args, kwargs = self._run_pre_adaptor(*args, **kwargs)
        args = list(args)
        res = []
        args_i = deepcopy(args)

        for i in args[0]:
            args_i[0] = i
            res_i = self(*args_i, **kwargs)
            if isinstance(res_i, list):
                res.extend(res_i)
            else:
                res.append(res_i)
        res = self._run_postf_adaptor(self._run_postf_filter(res))
        self._run_dumper(deepcopy(res))
        return res

    def __call__(self, *args, **kwargs):
        # if self._source:
        #     args = list(args)
        #     args.insert(self._source())

        args, kwargs = self._run_pre_filter(*args, **kwargs)
        args, kwargs = self._run_pre_adaptor(*args, **kwargs)
        res = self._run_postf_adaptor(
            self._run_postf_filter(self._func(*args, **kwargs)))
        self._run_dumper(deepcopy(res))
        return res


class MultiWrapper():
    def __init__(self, func, crontab: str = None, *args, **kwargs):
        super(MultiWrapper, self).__init__()
        self._func = func
        self._crontab = crontab
        self._source = None
        self._args = args
        self._kwargs = kwargs
        # if self._crontab_expr:
        # self._crontab_iter = croniter(self._crontab_expr, datetime.now())
    @staticmethod
    def _crontab_run(expr: str, t_func, _args, _kwargs):
        '''
        crontab定时功能
        '''
        crontab_history = deque(maxlen=7)
        crontab_iter = croniter(expr, datetime.now())
        while True:
            this_crontab_datetime = crontab_iter.get_next(datetime)
            if this_crontab_datetime not in crontab_history:
                crontab_history.append(this_crontab_datetime)
                t_func(*_args, **_kwargs)
                t_func(*_args, **_kwargs).start()
            time.sleep(1)

    def set_source(self, source):
        self._source = source

    def set_logger_handle(self, path: str, police_or_not=False):
        self.run = log_file_hook(path)(self.run)
        self._file_logger_or_not = True
        self._police_or_not = police_or_not

    @staticmethod
    def _t_func_maker(func):
        class TFunc(Thread):
            def __init__(self, func, *args, **kwargs):
                self._func = func
                self._args = args
                self._kwargs = kwargs

            def __call__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def run(self):
                self._func(*self._args, **self._kwargs)

        return TFunc(func)

    def __call__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs