# -*- coding: utf-8 -*-
__author__ = 'zciel'

import requests
from lxml import etree
import time
import pymongo as pm

# 获取连接
client = pm.MongoClient('mongodb://{0}:{1}@{2}:{3}'.format("root", "root", "47.99.160.128", 27017))

# 连接目标数据库
db = client.sun

headers = {
    "Host": "yglz.tousu.hebnews.cn",
    "Origin": "http://yglz.tousu.hebnews.cn"
}
try:
    response = requests.post("http://yglz.tousu.hebnews.cn/l-1001-5-")
    html = response.content.decode("utf-8")
except Exception as e:
    print(e)

# 解析html
tree = etree.HTML(html)

hids = tree.xpath('//input[@type="hidden"]')

common_param = {}

for ipt in hids:
    common_param.update({ipt.get("name"): ipt.get("value")})  # update有相同的键就覆盖，没有就添加

# 总共有1005页数据 死循环
for i in range(1, 1005):
    common_param.update({"__CALLBACKPARAM": f"Load|*|{i}",
                         "__CALLBACKID": "__Page",
                         "__EVENTTARGET": "",
                         "__EVENTARGUMENT": ""})

    response = requests.post("http://yglz.tousu.hebnews.cn/l-1001-5-", data=common_param, headers=headers)
    html = response.content.decode("utf-8")
    print("*" * 200) #每一页的标志

    # 解析html
    tree = etree.HTML(html)  # 解析html
    divs = tree.xpath('//div[@class="listcon"]')
    for div in divs:
        try:
            shouli = div.xpath('span[1]/p/a/text()')[0]  # 受理单位
            type = div.xpath('span[2]/p/text()')[0].replace("\n", "")  # 投诉类型
            content = div.xpath('span[3]/p/a/text()')[0]  # 投诉内容
            datetime = div.xpath('span[4]/p/text()')[0].replace("\n", "")  # 时间
            status = div.xpath('span[6]/p/text()')[0].replace("\n", "")  # 状态
            one_data = {"shouli": shouli,
                        "type": type,
                        "content": content,
                        "datetime": datetime,
                        "status": status,
                        }
            print(one_data)
            db.wenzheng.insert_one(one_data)  # 插入单个文档
        except Exception as e:
            print("内部数据报错")
            print(div)
            continue
        print("数据插入成功{}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
        time.sleep(2) #睡眠2秒钟

