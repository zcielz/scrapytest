# -*- coding: utf-8 -*-
__author__ = 'zciel'

import re

s1 = '我12345+aBCde'
# pattern字符串前加 “ r ” 表示原生字符串
pattern = r'(\w+)\+(\w+)'
# 返回一个匹配的列表
result1 = re.findall(pattern, s1, re.IGNORECASE)  # 蒲培不区分大小写
print(result1)
