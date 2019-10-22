# -*- coding: utf-8 -*-
__author__ = 'zciel'
import requests

def run():
    response = requests.get("http://www.baidu.com")
    print(response.text)

if __name__ == "__main__":
    run()