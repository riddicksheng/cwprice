# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 18:10
# @Author  : Riddick_Li+
# @File    : common.py
# @Software: PyCharm Edu

import hashlib


def get_md5(input_str):

    if isinstance(input_str, str):
        input_str = input_str.encode("utf-8")
    m = hashlib.md5()
    m.update(input_str)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5("hello"))
