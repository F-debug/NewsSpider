import time
import datetime
from scrapy import cmdline

def runifengnews(h, m):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if (now.hour == h and now.minute >= m) or (now.hour > h):
                break
            # 不到时间就等10秒之后再次检测
            time.sleep(10)

        cmdline.execute("scrapy crawl ifengnews -o 凤凰新闻0106_1.csv".split())

runifengnews(8, 38)