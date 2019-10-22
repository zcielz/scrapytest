# -*- coding: utf-8 -*-
__author__ = 'zciel'

import pymongo as pm

# 获取连接
client = pm.MongoClient('mongodb://{0}:{1}@{2}:{3}'.format("root", "root", "47.99.160.128", 27017))

# 连接目标数据库
db = client.dm

# 数据库用户验证
# db.authenticate("root", "root")

post = {
    "id": "111111",
    "level": "MVP",
    "real": 1,
    "profile": '111',
    'thumb': '2222',
    'nikename': '222',
    'follows': 20
}

db.col.insert_one(post)  # 插入单个文档

# 打印集合第1条记录
print(db.col.find_one())
