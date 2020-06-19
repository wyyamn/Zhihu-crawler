# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 20:13:22 2020

@author: natuk
"""

from Autologin import Zhihu
from HotChart import rankings, wordcloud  
from selenium import webdriver
from playsound import playsound
import pandas as pd #读取文件用
import time
import os


global vis_browser  # 把可视化的网页设成全局变量

if __name__ == "__main__":
    chromedriver_path = "C:\\Users\\natuk\\Anaconda3\\Scripts\\chromedriver.exe"
    viz_browser = webdriver.Chrome()
    viz_browser.minimize_window()
    
    #读取配置文件
    config = pd.read_csv('C:\\Users\\natuk\\Desktop\\北大\\计算机科学与编程入门\\1700091817_翁雨音_final\\config.csv')
    kw = pd.read_csv('C:\\Users\\natuk\\Desktop\\北大\\计算机科学与编程入门\\1700091817_翁雨音_final\\Keywords.csv')
    
    refresh_time = config['refresh_seconds'].item()  # 刷新时间控制
    keywords_list = [] #关键词列表
    for item in kw['Keyword']:
        keywords_list.append(item)
    
    is_open = False  # Flag的原始状态是“网页已打开”
    
    while True:
        zhihu = Zhihu()
        zhihu.use_cookie()
        rankings()
        print('已抓取最新热榜')
        wordcloud()
        print('最新词云已生成')
        
        if not is_open:
            print('正在打开本地的网页') #如果本地网页没打开，就打开
            local_url = 'file:///' + os.path.abspath('zhihu_wordcloud.html')
            viz_browser.maximize_window()
            viz_browser.get(local_url)
            is_open = True
        else:
            print('刷新网页中...') #如果本地网页已经打开，就刷新
            viz_browser.refresh()
        t = refresh_time
        time.sleep(t)
        
         # 事先设定的关键词有没有出现
        with open('C:\\Users\\natuk\\Desktop\\北大\\计算机科学与编程入门\\1700091817_翁雨音_final\\zhihu_hot.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            cnt = 0  # 用来记录正在读第几行
            cnt_list = []  # 用来记录第几行出现了关键词
            for line in lines:
                cnt += 1
                for keyword in keywords_list:
                    if keyword in line:
                        print("第  %d  条热搜里面出现了关键词  %s !!" % (cnt, keyword))
                        cnt_list.append(cnt)
                        playsound('ringtone.mp3')
                        break