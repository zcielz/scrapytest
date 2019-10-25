# -*- coding: utf-8 -*-
__author__ = 'zciel'

import re

s1 = '我12345+abcde'
# pattern字符串前加 “ r ” 表示原生字符串
pattern = r'(\w+)\+(\w+)'
pattern_compile = re.compile(pattern)
# 返回匹配的字符串
result1 = re.match(pattern_compile, s1).group()
# 返回匹配开始的位置
result2 = re.match(pattern_compile, s1).start()
# 返回匹配结束的位置
result3 = re.match(pattern_compile, s1).end()
# 返回一个元组包含匹配（开始，结束）位置
result4 = re.match(pattern_compile, s1).span()

print(result1)
print(result2)
print(result3)
print(result4)
