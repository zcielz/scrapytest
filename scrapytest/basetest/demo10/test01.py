# -*- coding: utf-8 -*-
__author__ = 'zciel'

import queue
import threading

# 全局变量，标识爬取状态
CRAWL_EXIT = False
url_format = ''


class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue):
        # threading.Thread.__init__(self)
        # 调用父类的初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        print(self.threadName + '启动 *******')
        while not CRAWL_EXIT:
            try:
                global tag, url, headers, img_format  # 把全局的值都拿过来
                # 队列为空 产生异常
                page = self.page_queue.get(block=False)  # 从里面获取值
                spider_url = url_format.format(tag, page, 100)  # 拼接要爬取的URL
                print(spider_url)
            except Exception as e:
                print(e)
                break



def main():
    # 声明一个队列，使用循环在里面存入100个页码
    page_queue = queue.Queue(100)
    for i in range(1, 101):
        page_queue.put(i)

    # 采集结果（等待下载的图片地址)
    data_queue = queue.Queue()

    # 记录线程的列表
    thread_crawl = []

    # 每次开启四个线程
    craw_list = ['采集线程1号', '采集线程2号', '采集线程3号', '采集线程4号']
    for thread_name in craw_list:
        c_thread = ThreadCrawl(thread_name, page_queue, data_queue)
        c_thread.start()
        thread_crawl.append(c_thread)

    # 等待page_queue队列为空，也就是等待之前的操作执行完毕
    while not page_queue.empty():
        pass


if __name__ == '__main__':
    main()
