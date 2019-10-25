# -*- coding: utf-8 -*-
__author__ = 'zciel'

import re

s1 = '我12345abcde'
s2 = '+?!@12345abcde'
# pattern字符串前加 “ r ” 表示原生字符串
pattern = r'\w.+'
pattern_compile = re.compile(pattern)
result1 = re.search(pattern_compile, s1)
result2 = re.search(pattern_compile, s2)
print(result1)
print(result2)
