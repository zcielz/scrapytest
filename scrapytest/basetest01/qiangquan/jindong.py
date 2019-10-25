# -*- coding: utf-8 -*-
__author__ = 'zciel'

from selenium import webdriver

# 打开chromer浏览器
browser = webdriver.Chrome()

browser.get("https://www.taobao.com")
browser.find_element_by_link_text("亲，请登录").click()

browser.get("https://cart.taobao.com/cart.htm")
browser.find_element_by_id("J_SelectAll1").click()
browser.find_element_by_link_text("结 算").click()