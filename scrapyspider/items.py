# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class newsItem(Item):   # 新闻内容包含以下属性
    # 文章标题
    title = Field()
    # 时间
    date = Field()
    # 正文
    content = Field()
    #简介（20个字）
    abstract = Field()
    # 文章热度（参与数）
    heat = Field()
    # ID
    id = Field()
    # 链接
    url = Field()
    # 评论字典
    comments = Field()




