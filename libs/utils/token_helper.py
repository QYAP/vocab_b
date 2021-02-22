# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 10:26
# @File    : token_helper.py
# @Software: PyCharm


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous.exc import SignatureExpired
# from itsdangerous.exc import BadSignature


def create_token(user_id: str, expires: int, salt: str) -> str:
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(salt, expires_in=expires)
    # 接收用户id转换与编码
    token = s.dumps({"user_id": user_id}).decode("ascii")
    return token


def verify_token(token: str, salt: str) -> dict:
    '''
    :return: 用户信息 or None
    '''

    s = Serializer(salt)
    data = s.loads(token)

    return data
