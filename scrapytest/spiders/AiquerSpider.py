# -*- coding: utf-8 -*-
__author__ = 'zciel'

import scrapy
from scrapy.http import Request


class AiquerSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'AiQuerSpider'
    # allowed_domains 定义访问域
    allowed_domains = ['iqiyi.com']
    # base_url定义要爬虫的网站
    bash_url = 'http://www.iqiyi.com/u/'
    # 做拼接地址的结尾
    bashurl = '/v?page=1'
    user_id = None

    # 用来获取输入的用户编号返回的凭借地址
    def start(self):
        self.user_id = self.validateIsNull(input(u'请输入用户编号:'))
        if self.user_id:
            url = self.bash_url + self.user_id + self.bashurl
            return url

    def start_requests(self):
        # 首先获取用户首页地址
        url = self.start()
        # Request函数第一个是地址，第二个是调用方法
        yield Request(url, self.max_page)

    # 这个方法是必须有的 不然爬虫跑不起来
    def parse(self, response):
        pass
