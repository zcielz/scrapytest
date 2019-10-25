# -*- coding: utf-8 -*-
__author__ = 'zciel'

import re

s1 = '我12345abcde'
s2 = '.12345abcde'
pattern = r'\w.+'
# 编译pattern
pattern_compile = re.compile(pattern)
# 对s1和s2分别匹配
result1 = re.match(pattern_compile, s1)
result2 = re.match(pattern_compile, s2)
print(result1)
print(result2)
print(s1.__len__())
