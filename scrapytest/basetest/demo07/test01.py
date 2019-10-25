# -*- coding: utf-8 -*-
__author__ = 'zciel'

import asyncio
import json
import re

import aiohttp


# 使用Asyncio + Aiohttp异步IO
async def fetch_img_url(num):
    url = f'http://bbs.fengniao.com/forum/forum_101_{num}_lastpost.html'
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400',
    }

    async with aiohttp.ClientSession() as session:
        # 获取轮播图的地址
        async with session.get(url, headers=headers) as response:
            try:
                url_format = "http://bbs.fengniao.com/forum/pic/slide_101_{0}_{1}.html"
                html = await response.text()  # 获取到网页源码
                print(html)
                pattern = re.compile('<div class="picList">([\s\S.]*?)</div>')
                first_match = pattern.findall(html)
                href_pattern = re.compile('href="/forum/(\d+?)_p(\d+?)\.html')
                urls = [url_format.format(href_pattern.search(url).group(1), href_pattern.search(url).group(2)) for url
                        in first_match]  # TDOD
                for img_slider in urls:
                    try:
                        async with session.get(img_slider, headers=headers) as slider:
                            slider_html = await slider.text()  # 获取到页面的源码
                            try:
                                pic_list_pattern = re.compile('\[(.*)?\]')
                                pic_list = "[{}]".format(pic_list_pattern.search(slider_html).group(1))
                                pic_json = json.loads(pic_list)  # 图片列表已经拿到
                                print(pic_json)
                            except Exception as e:
                                print("代码调试错误")
                                print(pic_list)
                                print("*" * 100)
                                print(e)

                            for img in pic_json:
                                try:
                                    img = img["downloadPic"]
                                    async with session.get(img, headers = headers) as img_res:
                                        imgcode = await img_res.read()
                                        with open("F:/source/python/code/scrapytest/scrapytest/basetest/demo07/downs/{}".format(img.split('/')[-1]), 'wb') as f:
                                            f.write(imgcode)
                                            f.close()
                                except Exception as e:
                                    print("图片下载错误")
                                    print(e)
                                    continue

                    except Exception as e:
                        print("基本错误")
                        print(e)
                        continue
                print("{}已经操作完毕".format(url))
            except Exception as e:
                print("基本错误")
                print(e)


# 这部分直接使用
# loop = asyncio.get_event_loop()
# tasks = asyncio.ensure_future(fetch_img_url(1))
# results = loop.run_until_complete(tasks)
loop = asyncio.get_event_loop()  # 这三行代码同上面代码
tasks = [fetch_img_url(1)]
results = loop.run_until_complete(asyncio.wait(tasks))
