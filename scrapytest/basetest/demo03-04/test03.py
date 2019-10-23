# -*- coding: utf-8 -*-
__author__ = 'zciel'

import pandas as pd
import requests
import re
import math
import os
import time

# url
base_url = "http://www.moko.cc{}"

# 用户图片表的模板
user_list_url = "http://www.moko.cc/post/{}/list.html"

# 存放所有的用户的列表页
user_profiles = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
all_pages = []


# 读取基本数据
def read_data():
    # pandas从csv里面读取数据
    df = pd.read_csv(r'F:/source/python/code/scrapytest/scrapytest/basetest/demo03/moko70000.csv')
    # 去掉昵称重复的 数据
    df = df.drop_duplicates(["nikename"])
    # 按照粉丝数目进行降序
    profiles = df.sort_values("follows", ascending=False)["profile"]

    for i in profiles:
        # 拼接链接
        user_profiles.append(user_list_url.format(i))


# 获取图片列表页面
def get_img_list_page(user_url):
    # 固定一个地址，方便测试
    # test_url = "http://www.moko.cc/post/da39db43246047c79dcaef44c201492d/list.html"
    try:
        response = requests.get(user_url, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        return
    page_text = response.text
    pattern = re.compile('<p class="title"><a hidefocus="ture".*?href="(.*?)" class="mwC u">.*?\((\d+?)\)</a></p>')
    # 获取 page_list
    page_list = pattern.findall(page_text)
    for page in page_list:
        if page[1] == '0':
            page_list.remove(page)
            continue
        else:
            get_all_list_page(page[0], page[1])


# 获取所有的页面
def get_all_list_page(start_page, totle):
    page_count = math.ceil(int(totle) / 28) + 1
    for i in range(1, page_count):
        pages = re.sub(r'\d+?\.html', str(i) + ".html", start_page)
        all_pages.append(base_url.format(pages))

    print("已经获取到的{}条数据".format(len(all_pages)))
    if (len(all_pages) > 1000):
        pd.DataFrame(all_pages).to_csv("./pages.csv", mode="a+")  # 通过pd.DataFrame设计成数据列， #todo mode a+用法
        all_pages.clear()


# 读取所有的数据
def read_list_data():
    # 读取数据
    img_list = pd.read_csv("./pages.csv", names=["no", "url"])["url"]

    # 循环操作数据
    for img_list_page in img_list:
        try:
            response = requests.get(img_list_page, headers=headers, timeout=3)
        except Exception as e:
            print(e)
            continue
            # 正则表达式获取页面图片列表页面
        pattern = re.compile('<a hidefocus="ture" alt="(.*?)".*? href="(.*?)".*?>VIEW MORE</a>')
        img_box = pattern.findall(response.text)

        need_links = []  # 每个用户个人中心待抓取的图片文件夹
        for img in img_box:
            print(img)
            need_links.append(img)

            # 创建目录
            file_path = "F:/source/python/code/scrapytest/scrapytest/basetest/demo03/downs/{}".format(
                re.sub('[\/\.\*\~\?\:\(\)\*<>|]', '', str(img[0])).strip())

            if not os.path.exists(file_path):
                os.makedirs(file_path)  # 创建目录

        for need in need_links:
            get_my_imgs(base_url.format(need[1]), need[0])


# 获取详情页面数据
def get_my_imgs(img, title):
    print(img)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    try:
        response = requests.get(img, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        return
    pattern = re.compile('<img src2="(.*?)".*?>')
    all_imgs = pattern.findall(response.text)
    for download_img in all_imgs:
        downs_imgs(download_img, title)


# 下载图片
def downs_imgs(img, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    try:
        response = requests.get(img, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        return
    content = response.content
    file_name = str(int(time.time())) + ".jpg"
    file = "./downs/{}/{}".format(re.sub('[\/\.\*\~\?\:\(\)\*<>|]', '', str(title)).strip(), file_name)
    try:
        with open(file, "wb+") as f:
            f.write(content)
    except Exception as e:
        print(e)
        return
    print("完毕")


if __name__ == '__main__':
    # 读取文件
    # read_data()
    # for user in user_profiles:
    #     get_img_list_page(user)

    # 开始处理文件
    read_list_data()
