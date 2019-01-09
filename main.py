  # -*- coding: utf-8 -*-

from scrapy.cmdline import execute

import sys
import os
import time

"""
add test

"""

start = time.time()
execute(["scrapy", "crawl", "cwprice"])
end = time.time()
# elapsed = (end - start)/60
# print("Time used :", elapsed, ' 秒')
# test  pro
