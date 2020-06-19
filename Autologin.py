# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:15:32 2020

@author: natuk
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as ex
import time
import os
import json  # 用于保存cookies
from random import random  # 用于生成乱数


class Zhihu:

    def __init__(self):
        url = 'https://www.zhihu.com/'
        self.url = url
        options = webdriver.ChromeOptions()
        
        self.browser = webdriver.Chrome(options=options)  
        self.chromedriver_path = "C:\\Users\\natuk\\Anaconda3\\Scripts\\chromedriver.exe"
        
        options.add_argument('disable-infobars') #去掉警告窗口        
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    # 检测是否登陆了知乎
    def is_login(self):
        try:
            return bool(
                self.browser.find_element_by_css_selector(".GlobalSideBar-navText")
            )
        except ex.NoSuchElementException:
            return False

    # 首次登录获取cookies
    def save_cookie(self):
        self.browser.get("https://www.zhihu.com/signin")
        
        print('请扫码登录后按回车...') # 手动扫码，登陆进去以后获取cookies
        
        cnt = 0
        while not self.is_login():
            time.sleep(random()) 
            cnt += 1
            print("第 %d 次尝试登录知乎" % cnt) # 直到登录成功为止，随机间隔连续尝试

        cookies = self.browser.get_cookies()  # 获取cookies
        print("cookies获取成功！")
        self.browser.close()
        with open('my_cookies1.json', 'w',encoding='utf-8') as f:
            f.write(json.dumps(cookies))

    #用本地cookie登录
    def use_cookie(self):
        print("本地已有cookies，可以直接登录")

        with open('my_cookies1.json', 'r', encoding='utf-8') as f:
            cookie_list = json.loads(f.read())  # 获取本地保存的cookies

        cookies_dict = dict()  # 把获取的cookies处理成dict类型
        for cookie in cookie_list:
            cookies_dict[cookie['name']] = cookie['value'] #把需要的要素提取出来

        self.browser.get("https://www.zhihu.com")
        for item in cookies_dict:
            self.browser.add_cookie({
                "domain": ".zhihu.com",
                "name": item,
                "value": cookies_dict[item],
                "path": '/',
                "expires": None
            })
        self.browser.get("https://www.zhihu.com")
        print("成功使用cookies登陆知乎！ 10秒后自动关闭")
        time.sleep(10)
        self.browser.close()


if __name__ == "__main__":
    chromedriver_path = "C:\\Users\\natuk\\Anaconda3\\Scripts\\chromedriver.exe"  # 改成你的chromedriver的完整路径地址

    zhihu = Zhihu()  #Class

    file = 'my_cookies1.json'
    if file not in os.listdir(): #如果当地没有cookie就重新获取
        zhihu.save_cookie()
    zhihu.use_cookie()