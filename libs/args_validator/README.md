# 参数校验

### cook-book
+ Validator(args,rule-dict,redundant_or_not=True, redundant_max_num=0).execute() 进行参数校验
+ rule-dict为一个字典
+ rule-dict的k值为字符串、Required(str)或Default(str)
+ rule-dict中k值为Default(arg)表示该参数为必须参数，k值为arg等效于Required(arg)
+ rule-dict中k值为Default(arg)表示该参数为可缺省参数
+ rule-dict的v值必须为一个类，或者BaseType及其子类
+ BasseType及其子类为模块自定义类，有Number、Enumeration、RegEx、Operator等
+ rule-dict的v值常为python基础的数据类型，等效于Type(基础的数据类型)，Type为模块自定义类
+ redundant_or_not表示是否允许args冗余，默认为True
+ redundant_max_num表示在可冗余的情况下，允许的冗余的参数数量，默认为无穷大
+ flask_plus_in.args_validator为flask插件，使用方式示例为如下：  
```python3
@app.route("/hello-world")
@args_validator(rule={"a": Number},redundant_or_not=True, redundant_max_num=3)
def hello_world():
    return 'Hello World!'
```


### 模块类介绍
+ Required      规则约束类，被修饰参数为必须参数，不可缺省
+ Default       规则约束类，被修饰参数为可缺省参数
+ Validator     校验类，功能包括规则字典校验与格式化、参数校验、冗余校验
+ Type          参数类型约束类，除python内置基础类型外，自定义的参数校验类型，包括Number、Enumeration、RegEx、Operator等
 

### 功能枚举
1，必须与可缺省校验功能
2，参数冗余校验功能
3，Python内置类型校验功能（int、float、complex、bool、str、tupple、list、set、dict、None）
4，自定义类型校验（Number、Enumeration、RegEx、Operator等）
5，校验接口
6，flask视图函数扩展插件
7，函数扩展插件（支持PEP484,PEP526,PEP3107等）
8，类扩展插件
9，多层参数校验功能
10，help文本查看功能

### 迭代开发计划
周期一（已完成）：
1，必须与可缺省校验功能
2，参数冗余校验功能
3，Python内置基础类型校验功能（缺None值校验）
4，自定义类型校验（Number）
4，flask视图函数扩展插件

周期二：
1，None校验
2，自定义类型校验（Enumeration）
3，校验接口

周期三：
1，help功能
2，自定义参数校验（Operator，RegEx）
3，函数扩展插件（PEP484）

周期四：
1，类扩展插件


