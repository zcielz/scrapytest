# -*- coding: utf-8 -*-
__author__ = 'zciel'

import re

s1 = '我12345+abcde'
# pattern字符串前加 “ r ” 表示原生字符串
pattern = r'(\w+)\+(\w)'
pattern_compile = re.compile(pattern)
# 返回含有所有子组的元组
result1 = re.search(pattern_compile, s1).groups()
print(result1)
a = [1,2]
print(a)
a.append(3)
print(a)

