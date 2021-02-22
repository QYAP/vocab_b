### Python 日志组件Logger

### 主要类介绍如下：
+ Factory   工厂类，负责生成Logger实例，主要工作还有校验、格式化config参数。
+ Logger    日志核心类，所有的日志都有该类进行处理
+ Record    记录类，产生所有的日志记录，主要工作还有收集日记的环境信息
+ ***Handle    终端处理类，处理所有的日志记录终端输出，包括缓存、染色、文件分割等



### 功能枚举：
1，日志等级控制输出  
2，日志记录自定义格式化  
3，日志染色（console端）  
4，日志记录缓存  
5，多端输出（控制台、文件输出、mongodb端、redis端、mysql端、email端、短信端、web可视化端）  
6，Web端可视化查看  
7，文件端文件分割、自动清理  
8，config参数校验提醒  
9，help文本查看功能  

### 迭代计划：
周期一：（已完成）
1，日志等级控制输出  
2，日志记录自定义格式化  
3，console输出（染色功能）  
4，日志记录缓存控制  

周期二：
1，Config参数校验  
2，help文本查看功能  
3，文件端输出  

周期三：
1，mongodb端输出  
2，redis端输出  

周期四：
1，web端可视化查看  
