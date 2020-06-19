# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 21:07:30 2020

@author: natuk
我发现知乎热榜不登录也可以看到，这个无登录版程序使得没有知乎账号的人也能热榜抓取
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

#抓取热榜---------------------------------

def rankings():
    chromedriver_path = "C:\\Users\\natuk\\Anaconda3\\Scripts\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)   
    #options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
    
    browser.get('https://www.zhihu.com/billboard')
    #获取页面内容
    html = browser.page_source

    ranking_title = re.findall(r'class="HotList-itemTitle">(.*?)</div>',html)
    ranking_amount = re.findall(r'class="HotList-itemMetrics">(.*?)</div>',html)
#<div class="HotList-itemTitle">如何看待进口三文鱼切割案板检测出新冠病毒？后续生鲜食品等的进口会被限制或暂停吗？</div>
#<div class="HotList-itemMetrics">6015 万热度</div>

    cnt = 1
    with open('C:\\Users\\natuk\\Desktop\\北大\\计算机科学与编程入门\\1700091817_翁雨音_final\\zhihu_hot.txt', 'w', encoding='utf-8') as f:
        for title,amount in zip(ranking_title,ranking_amount):
            print(str(cnt) + '. ' + title + '(' + str(amount) + ')')
            print(str(cnt) + '. ' + title + '(' + str(amount) + ')', file=f)
            cnt += 1
        print('已更新热榜记录')

if __name__ == "__main__":
    rankings()

#生成词云----------------------------------

from pyecharts import options as opts
from pyecharts.charts import WordCloud

def wordcloud():
    latest_time = os.path.getmtime("C:\\Users\\natuk\\Desktop\\北大\\计算机科学与编程入门\\1700091817_翁雨音_final\\zhihu_hot.txt")  # Unix时间
    latest_time = time.localtime(latest_time)
    latest_time = time.strftime("%Y-%m-%d %H:%M:%S", latest_time) #转换为年-月-日-时-分-秒的形式
    latest_time = str(latest_time)
    #  print(latest_time)

    data = []
    
    with open("C:\\Users\\natuk\\Desktop\\北大\\计算机科学与编程入门\\1700091817_翁雨音_final\\zhihu_hot.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            s1 = line.split('.')[1] # 去掉序号
            title = s1.split('(')[0]
            s2 = s1.split('(')[1]
            amount_s = s2.split('万热度')[0]
            amount = int(amount_s)
            #print(title, amount)
            data.append((title,amount))
                    
    #print(data)
            
    
    (
        WordCloud()
        .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="热点分析 更新于 " + latest_time, 
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .render("zhihu_wordcloud.html")
    )

if __name__ == "__main__":
    wordcloud()
