# -*- coding: utf-8 -*-
__author__ = 'zciel'

import requests
import threading  # 多线程模块
import re  # 正则表达式模块
import time  # 时间模块
import os  # 目录操作模块

# 这里定义全局变量
all_urls = []  # 我们拼接好的图片集和列表路径
all_img_urls = []  # 图片列表页面的数组
pic_links = []  # 图片地址列表
g_lock = threading.Lock()  # 初始化一个锁


class Producer(threading.Thread):  # threading.Thread中继承了一个子类
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'HOST': 'www.meizitu.com'
        }
        global all_urls  # 使用拼接好的图片集合列表路径
        while len(all_urls) > 0:
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            page_url = all_urls.pop()  # 通过pop方法移除最后一个元素，并且访问该值

            g_lock.release()  # 使用完后讲锁释放，方便其他线程使用
            try:
                print("分析" + page_url)
                response = requests.get(page_url, headers=headers, timeout=3)
                all_pic_link = re.findall('<a target=\'_blank\' href="(.*?)">', response.text, re.S)  # 使用正则表达式匹配
                global all_img_urls
                g_lock.acquire()  # 设置锁
                all_img_urls += all_pic_link  # 这里地方主义数组拼接，没有使用append直接使用+=
                print(all_img_urls)
                g_lock.release()  # 释放锁
                time.sleep(0.5)
            except:
                pass


# 消费者
class Consumer(threading.Thread):
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'HOST': 'www.meizitu.com'
        }
        global all_img_urls  # 调用全局的图片详情页面介绍
        print("%s is running" % threading.current_thread())
        while len(all_img_urls) > 0:
            g_lock.acquire()
            img_url = all_img_urls.pop()
            g_lock.release()
            try:
                response = requests.get(img_url, headers=headers)
                response.encoding = 'gb2312'  # 由于我们调用的页面编码是gb2312，所有这里要统一设置编码
                title = re.search('<title>(.*?) | 妹子图</title>', response.text).group(1)
                all_pic_src = re.findall('<img alt=.*?src="(.*?)" /><br />', response.text, re.S)

                pic_dict = {title: all_pic_src}  # python字典
                global pic_links
                g_lock.acquire()
                pic_links.append(pic_dict)
                print(title + " 获取成功")
                g_lock.release()

            except:
                pass
            time.sleep(0.5)


class DownPic(threading.Thread):
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'HOST': 'www.meizitu.com'
        }

        while True:
            global pic_links
            # 上锁
            g_lock.acquire()
            if len(pic_links) == 0:
                # 不管什么情况，都要释放锁
                g_lock.release()
                continue
            else:
                pic = pic_links.pop()
                g_lock.release()
                # 遍历字典列表
                for key, values in pic.items():
                    path = key.rstrip("\\")
                    is_exists = os.path.exists(path)
                    # 判断结果
                    if not is_exists:
                        # 如果不存在则创建目录
                        # 创建目录操作函数
                        os.makedirs(path)

                        print(path + '目录创建成功')

                    else:
                        # 如果目录存在则不创建，并提示目录已存在
                        print(path + ' 目录已存在')
                    for pic in values:
                        filename = path + "/" + pic.split('/')[-1]
                        if os.path.exists(filename):
                            continue
                        else:
                            try:
                                response = requests.get(pic, headers=headers)
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                                    f.close
                            except Exception as e:
                                print(e)
                                pass


class Spider:
    # 构造函数，初始化数据使用
    def __init__(self, target_url, headers):
        self.target_url = target_url
        self.headers = headers

    # 获取所有的想要抓取的URL
    def getUrls(self, start_page, page_num):
        # 全局变量 存储我们的所有分页的URL
        global all_urls
        # 循环得到URL
        for i in range(start_page, page_num + 1):
            url = self.target_url % i
            all_urls.append(url)


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'HOST': 'www.meizitu.com'
    }
    target_url = 'http://www.meizitu.com/a/pure_%d.html'  # 图片集和列表规则

    spider = Spider(target_url, headers)
    spider.getUrls(1, 16)
    print(all_urls)
    threads = []
    for x in range(2):
        t = Producer()
        t.start()
        threads.append(t)

    for tt in threads:
        tt.join()  # 主线程遇到join之后进入阻塞状态,一直等待其他的子线程执行结束之后，主线程在继续执行。

    # 开启10个线程去获取链接
    for x in range(10):
        ta = Consumer()
        ta.start()

    # 开启10个线程保存图片
    for x in range(10):
        down = DownPic()
        down.start()

    print("进行到我这里了")
