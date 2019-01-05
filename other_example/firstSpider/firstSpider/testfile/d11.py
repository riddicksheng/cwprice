# -*- coding: utf-8 -*-
# @Time    : 2018/11/30 16:01
# @Author  : Riddick_Li+
# @File    : d11.py
# @Software: PyCharm Edu

import os


dirname = os.path.dirname(__file__)
abspath = os.path.abspath(dirname)

if __name__ == "__main__":
    print(dirname)
    print(abspath)
    print(os.path.join(abspath, "images"))
