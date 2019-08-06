import time
import datetime
from scrapy import cmdline

def runqqnews(h, m):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if now.hour >= h and now.minute >= m:
                break
            # 不到时间就等10秒之后再次检测
            time.sleep(10)

        cmdline.execute("scrapy crawl qqnews -o 腾讯新闻0106_1.csv".split())

runqqnews(8, 0)