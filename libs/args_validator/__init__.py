# encoding: utf-8
# Author    : AP
# Datetime  : 2019/7/23 16:31
# Project   : RBAC

from ._type import BaseType, Type
from ..exception.args.validator import ArgsValidatorError


# 基本key约束，转成tupple处理，0，1分别表示可缺省
def Required(arg_name: str):
    """
        不可缺省的参数，默认为不可缺省参数
    """
    return (1, arg_name)


def Default(arg_name: str):
    """
        可缺省的参数
    """
    return (0, arg_name)


class Validator():
    def __init__(self, args: dict, rule: dict, redundant_or_not: bool = True, redundant_max_num: int = float("inf")):
        self.args = args
        self.rule = rule
        self.redundant_or_not = redundant_or_not
        self.redundant_max_num = redundant_max_num
        self.args_num = len(args)
        self.rule_num = len(rule)
        self.lack_default_num = 0

    def standard_rule(self):
        '''
        This function will convert user's input to stardard rule-dict.
        User can input key of rule-dict with str or Required(str) or default(str).
        User can input value of rule-dict with commom class or instance of BaseType'sub-class.
        Rule-dict's stardard format is {(stant:int,arg_name:str):BaseType'sub-class()}

        Raises:
            rule-dict key error
            rule-dict value error
        '''

        # 检查并标准化规则字典（必须先检查v值，再检查k值，然后规范化k,v值，顺序不能颠倒）
        for arg_name, arg_type in list(self.rule.items()):

            # rule-dict 的v值必须为一个类或者BaseType及其子类的一个实例
            if not isinstance(arg_type, type) and not issubclass(type(arg_type), BaseType):
                msg = "Rule-dict value error，rule-dict's value must be a class or instance of BaseType'sub-class!"
                raise ArgsValidatorError(msg)

            # 处理rule-dict key键为字符串的情况，并规范化value值
            if isinstance(arg_name, str):
                if not issubclass(type(arg_type), BaseType):
                    self.rule[Required(arg_name)] = Type(self.rule.pop(arg_name))
                else:
                    self.rule[Required(arg_name)] = self.rule.pop(arg_name)
            # 处理rule-dict key键为tupple的情况，并规范化value值
            elif isinstance(arg_name, tuple) and len(arg_name) == 2 and isinstance(arg_name[0], int) \
                    and isinstance(arg_name[1], str):
                if not issubclass(type(arg_type), BaseType):
                    self.rule[arg_name] = Type(arg_type)
                else:
                    self.rule[arg_name] = arg_type
            else:
                msg = "Rule-dict key error，rule-dict's key format error!"
                raise ArgsValidatorError(msg)

    def check_args(self):
        """
        This function will use rule-standarded to check args.
        """
        for arg_flag_name, arg_type in self.rule.items():
            # 如果该参数是必须参数
            if arg_flag_name[0] == 1:
                # 参数若存在则检查参数类型
                if arg_flag_name[1] in self.args:
                    if arg_type.process_flag == 0:
                        if type(self.args[arg_flag_name[1]]) not in arg_type.field:
                            raise ArgsValidatorError("args type error,type of %s should be %s!" %
                                                     (arg_flag_name[1], str(arg_type.field)))
                else:
                    msg = "Args lack error,lack %s" % arg_flag_name[1]
                    raise ArgsValidatorError(msg)
            # 如果该参数是可缺省参数
            elif arg_flag_name[0] == 0:
                if arg_flag_name[1] in self.args:
                    if arg_type.process_flag == 0:
                        if type(self.args[arg_flag_name[1]]) not in arg_type.field:
                            msg = "Args type error,type of %s  should be %s!" % (arg_flag_name[1], str(arg_type.field))
                            raise ArgsValidatorError(msg)
                else:
                    self.lack_default_num += 1

    def check_redundant(self):
        """
        This function will count args to check redundant or not.
        """
        redundant_num = self.args_num - (self.rule_num - self.lack_default_num)
        if self.redundant_or_not:
            if redundant_num > self.redundant_max_num:
                msg = "args redundant error,%s more  args were given!" % (redundant_num - self.redundant_max_num)
                raise ArgsValidatorError(msg)
        else:
            if redundant_num > 0:
                msg = "args redundant error,%s more  args were given!" % redundant_num
                raise ArgsValidatorError(msg)

    def execute(self):
        """
        This is the entry of Validator.
        """
        # 规范化参数校验规则字典
        self.standard_rule()
        # 根据规则字典校验参数
        self.check_args()
        # 检查冗余错误
        self.check_redundant()

# 测试代码：
# 测试rule-dict k值错误
# k不为字符串、Require(str)或Default(str)
# args = {"a": 1, "b": 2, "c": "3", 1: 1}
# rule_dict = {Required("a"): int, Default("b"): Type(int), 1: int}
# # Validator(args=args, rule=rule_dict).execute()
# try:
#     Validator(args=args, rule=rule_dict).execute()
# except Exception as e:
#     print(e, ":\tk不为字符串、Require(str)或Default(str)")

# # 测试rule-dict v值错误
# # v值为实例并且非BaseType子类实例
# args = {"a": 1, "b": 2, "c": 3, "d": 4, 1: 1}
# rule_dict = {Required("a"): int, Default("b"): Type(int), "c": Number, "d": 1}
# # Validator(args=args, rule=rule_dict).execute()
# try:
#     Validator(args=args, rule=rule_dict).execute()
# except Exception as e:
#     print(e, ":\tv值为实例并且非BaseType子类实例")

# # 测试args错误
# # 必须参数类型错误
# args = {"a": 1, "b": 2, "c": "3", "d": 4, 1: 1}
# rule_dict = {Required("a"): str, Default("b"): Type(int), "c": Number, "d": int}
# # Validator(args=args, rule=rule_dict).execute()
# try:
#     Validator(args=args, rule=rule_dict).execute()
# except Exception as e:
#     print(e, ":\targ必须参数类型错误")

# # 必须参数缺少
# args = {"b": 2, "c": "3", "d": 4, 1: 1}
# rule_dict = {Required("a"): str, Default("b"): Type(int), "c": Number, "d": int}
# # Validator(args=args, rule=rule_dict).execute()
# try:
#     Validator(args=args, rule=rule_dict).execute()
# except Exception as e:
#     print(e, ":\targ必须参数缺少错误")

# # 可缺省参数类型错误
# args = {"a": "1", "b": 2, "c": 3, 1: 1}
# rule_dict = {Required("a"): int, Default("b"): Type(int), "c": Number, Default("d"): int}
# # Validator(args=args, rule=rule_dict).execute()
# try:
#     Validator(args=args, rule=rule_dict).execute()
# except Exception as e:
#     print(e, ":\targ可缺省参数类型错误")

# # 参数冗余错误
# args = {"a": 1, "c": 3, 1: 1}
# rule_dict = {Required("a"): int, Default("b"): Type(int), "c": Number, Default("d"): int}
# # Validator(args=args, rule=rule_dict).execute()
# try:
#     Validator(args=args, rule=rule_dict, redundant_or_not=True, redundant_max_num=0).execute()
# except Exception as e:
#     print(e, ":\targ参数冗余错误")
