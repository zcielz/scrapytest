# -*- coding: utf-8 -*-
__author__ = 'zciel'

import os
import re
import threading
import time

import requests

import http_help as hh

urls_lock = threading.Lock()  # url操作锁
imgs_lock = threading.Lock()  # 图片操作锁  #，在多个线程之间操作全局变量，需要进行及时的锁定；

imgs_start_urls = []


# 1.获取网页源码
# 2.正则匹配末页元素
# 3.提取数字

# 获取所有待爬取的URL列表
class ImageList():
    def __init__(self):
        self.__start = "http://www.2717.com/ent/meinvtupian/list_11_{}.html"  # URL模板
        # 头文件
        self.__headers = {"Referer": "http://www.2717.com/ent/meinvtupian/",
                          "Host": "www.2717.com"
                          }
        self.__res = hh.R(headers=self.__headers)  # 初始化访问请求

    def run(self):
        page_count = int(self.get_page_count())

        if page_count == 0:
            return
        urls = [self.__start.format(i) for i in range(1, page_count)]
        return urls

    # 正则表达式匹配末页，分析页码
    def get_page_count(self):
        # 注意这个地方需要传入编码
        content = self.__res.get_content(self.__start.format("1"), "gb2312")
        pattern = re.compile("<li><a href='list_11_(\d+?).html' target='_self'>末页</a></li>")
        search_text = pattern.search(content)
        if search_text is not None:
            count = search_text.group(1)
            return count
        else:
            return 0


# 采用生产者和消费者模型，就是一个抓取链接图片，一个下载图片，采用多线程的方式进行操作
class Product(threading.Thread):
    # 类初始化方法
    def __init__(self, urls):
        threading.Thread.__init__(self)
        self.__urls = urls
        self.__headers = {"Referer": "http://www.2717.com/ent/meinvtupian/",
                          "Host": "www.2717.com"
                          }
        self.__res = hh.R(headers=self.__headers)

    # 链接抓取失败之后重新加入urls列表中
    def add_fail_url(self, url):
        print("{}该URL爬取失败".format(url))
        global urls_lock
        if urls_lock.acquire():
            self.__urls.insert(0, url)
            urls_lock.release()  # 解锁

    # 线程主要分昂发
    def run(self):
        print("*" * 100)
        while True:
            global urls_lock, imgs_start_urls
            if len(self.__urls) > 0:
                if urls_lock.acquire():  # 锁定
                    last_url = self.__urls.pop()  # 获取urls里面最后一个url，并且删除
                    urls_lock.release()  # 解锁
                print("正在操作{}".format(last_url))

                content = self.__res.get_content(last_url, "gb2312")  # 页面编码是gb2312
                if content is not None:
                    html = self.get_page_list(content)
                    if len(html) == 0:
                        self.add_fail_url(last_url)
                    else:
                        if imgs_lock.acquire():
                            imgs_start_urls.extend(html)  # 爬取图片之后，把他放在待下载的图片的列表中
                            imgs_lock.release()
                        time.sleep(5)
                else:
                    self.add_fail_url(last_url)
            else:
                print("所有链接已经运行完毕")
                break

    def get_page_list(self, content):
        # 正则表达式
        pattern = re.compile('<li><a href="(.*?)" title="(.*?)" class="MMPic" target="_blank">.*?</li>')
        list_page = re.findall(pattern, content)
        return list_page


# 实现图片的抓取
class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__headers = {"Referer": "http://www.2717.com/ent/meinvtupian/",
                          "Host": "www.2717.com"}

        self.__res = hh.R(headers=self.__headers)

    def download_img(self, filder, img_down_url, filename):
        file_path = "./downs/{}".format(filder)

        if not os.path.exists(file_path):
            os.mkdir(file_path)  # 创建目录
        if os.path.exists("./downs/{}/{}".format(filder, filename)):  # 如果包含就直接return
            return
        else:
            try:
                img = requests.get(img_down_url, headers={"Host": "t2.hddhhn.com"}, timeout=3)
            except Exception as e:
                print(e)
            print("{}写入图片".format(img_down_url))
            try:
                with open("./downs/{}/{}".format(filder, filename), "wb+") as f:
                    f.write(img.content)
            except Exception as e:
                print(e)
                return

    def run(self):
        while True:
            global imgs_start_urls, imgs_lock
            if len(imgs_start_urls) > 0:
                if imgs_lock.acquire():  # 锁定
                    img_url = imgs_start_urls[0]  # 获取到链接之后
                    del imgs_start_urls[0]  # 删除掉第0项
                    imgs_lock.release()  # 解锁
            else:
                continue
            # http://www.27270.com/ent/meinvtupian/2018/295631_1.html

            # print("图片开始下载")
            img_url = img_url[0]
            start_index = 1
            base_url = img_url[0:img_url.rindex(".")]

            while True:
                img_url = "{}_{}.html".format(base_url, start_index)
                content = self.__res.get_content(img_url, charset="gbk")
                if content is not None:
                    pattern = re.compile(
                        '<div class="articleV4Body" id="picBody">[\s\S.]*?img alt="(.*?)".*? src="(.*?)" />')
                    img_down_url = pattern.search(content)  # 获取到了图片地址
                    if img_down_url is not None:
                        filder = img_down_url.group(1)
                        img_down_url = img_down_url.group(2)

                        filename = img_down_url[img_down_url.rindex("/") + 1:]
                        self.download_img(filder, img_down_url, filename)  # 下载图片
                    else:
                        print("-" * 100)
                        print(content)
                        break  # 终止循环体
                else:
                    print("{}链接加载失败".format(img_url))
                    if imgs_lock.acquire():  # 锁定
                        imgs_start_urls.append(img_url)
                        imgs_lock.release()  # 解锁
                start_index += 1
                time.sleep(3)


if __name__ == "__main__":
    img = ImageList()
    urls = img.run()

    for i in range(1, 2):
        p = Product(urls)
        p.start()

    for i in range(1, 2):
        c = Consumer()
        c.start()
