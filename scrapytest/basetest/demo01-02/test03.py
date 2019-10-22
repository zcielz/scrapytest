# -*- coding: utf-8 -*-
__author__ = 'zciel'

import requests
# 下载图片
def run():
    response = requests.get("http://www.newsimg.cn/big201710leaderreports/xibdj20171030.jpg")
    with open("xijinping.jpg","wb") as f :
        f.write(response.content)
        f.close

if __name__ == "__main__":
    run()