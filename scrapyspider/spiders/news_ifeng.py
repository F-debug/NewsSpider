# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from ..items import newsItem
from scrapy.linkextractors import LinkExtractor
import re
import requests
import json
import time
from scrapy.selector import Selector


count = 49687


class NewsifengSpider(CrawlSpider):
    # 爬虫名称
    name = "ifengnews"
    # 伪装成浏览器
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.143 '
            'Safari/537.36'
    }
    # 全网域名
    allowed_domains = [
                       "ifeng.com"
    ]
    # 新闻版
    start_urls = [
       'http://www.ifeng.com/'
       # 'http://news.ifeng.com/a/20160411/48422258_0.shtml'
    ]
    # 可以继续访问的url规则,http://news.163.com/\d\d\d\d\d(/([\w\._+-])*)*$
    rules = [
        Rule(LinkExtractor(
            allow='http://.*.ifeng.com/a(/([\w\._+-])*)*$'
            # deny=('http://news.ifeng.com/snapshots(/([\w\._+-])*)*$')
        ),
            callback="parse_item",
            follow=True)
    ]
    def parse_item(self, response):
        global count
        # response是当前url的响应
        article = Selector(response)
        url = response.url

        # http://news.ifeng.com/a/20171228/54623520_0.shtml
        if get_category(article) == 1:
            articleXpath = '//*[@id="artical"]'
            if article.xpath(articleXpath):#如果文章页面存在
                titleXpath = '//*[@id="artical_topic"]/text()'
                dateXpath = '//*[@id="artical_sth"]/p/span[1]/text()'
                contentXpath = '//*[@id="main_content"]'
                news_infoXpath = '/html/head/script[10]/text()'
                # news_infoXpath2 = '/html/body/div[24]/script[1]/text()'
                # 标题
                if article.xpath(titleXpath):
                    news_item = newsItem()# 实例化条目
                    get_title(article, titleXpath, news_item)
                    news_item['url'] = url
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        try:
                            get_content(article, contentXpath, news_item)
                            count += 1
                            news_item['id'] = count
                        except:
                            return
                    # 评论
                    try:
                        comment_url = get_comment_url(article,url)
                        # 评论处理
                        comments = get_comment(comment_url, news_item)[1]
                        news_item['comments'] = comments
                    except:
                        news_item['comments'] = ' '
                        news_item['heat'] = 0
                    yield news_item

        # http://news.ifeng.com/a/20171228/54620295_0.shtml
        if get_category(article) == 2:
            articleXpath = '/html/body/div[3]'
            if article.xpath(articleXpath):  # 如果文章页面存在
                titleXpath = '/html/body/div[3]/div[1]/h1/text()'
                dateXpath = '/html/body/div[3]/div[1]/p/span/text()'
                contentXpath = '/html/body/div[3]/div[2]/div[1]/div[1]'
                contentXpath2 = '/html/body/div[3]/div[2]/div[1]'
                contentXpath3 = '//*[@id="yc_con_txt"]'
                # news_infoXpath = '/html/head/script[6]/text()'

                # 标题
                if article.xpath(titleXpath):
                    news_item = newsItem()# 实例化条目
                    get_title(article, titleXpath, news_item)
                    news_item['url'] = url
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        try:
                            get_content(article, contentXpath, news_item)
                            count += 1
                            news_item['id'] = count
                        except 1:
                            get_content(article, contentXpath2, news_item)
                            count += 1
                            news_item['id'] = count
                        except 2:
                            get_content(article, contentXpath3, news_item)
                            count += 1
                            news_item['id'] = count

                    # 评论
                    try:
                        comment_url = get_comment_url2(article, url)
                        # 评论处理
                        comments = get_comment(comment_url, news_item)[1]
                        news_item['comments'] = comments
                    except:
                        news_item['comments'] = ' '
                        news_item['heat'] = 0
                    yield news_item

        if get_category(article) == 3:
            articleXpath = '/html/body/div[4]'
            if article.xpath(articleXpath):  # 如果文章页面存在
                titleXpath = '/html/body/div[4]/div[2]/h1/text()'
                dateXpath = '//*[@id="artical_sth"]/p/span[1]/text()'
                contentXpath = '//*[@id="main_content"]'
                contentXpath2 = '/html/body/div[3]/div[2]/div[1]'
                contentXpath3 = '//*[@id="yc_con_txt"]'
                # news_infoXpath = '/html/head/script[6]/text()'

                # 标题
                if article.xpath(titleXpath):
                    news_item = newsItem()# 实例化条目
                    get_title(article, titleXpath, news_item)
                    news_item['url'] = url
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        try:
                            get_content(article, contentXpath, news_item)
                            count += 1
                            news_item['id'] = count
                        except 1:
                            get_content(article, contentXpath2, news_item)
                            count += 1
                            news_item['id'] = count
                        except 2:
                            get_content(article, contentXpath3, news_item)
                            count += 1
                            news_item['id'] = count

                    # 评论
                    try:
                        comment_url = get_comment_url2(article, url)
                        # 评论处理
                        comments = get_comment(comment_url, news_item)[1]
                        news_item['comments'] = comments
                    except:
                        news_item['comments'] = ' '
                        news_item['heat'] = 0
                    yield news_item

        if get_category(article) == 4:
            articleXpath = '/html/body/div[2]/div/div[3]'
            if article.xpath(articleXpath):  # 如果文章页面存在
                titleXpath = '/html/body/div[2]/div/div[3]/h1/text()'
                dateXpath = '/html/body/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/p[2]/text()'
                contentXpath = '/html/body/div[2]/div/div[3]/div[7]'
                contentXpath2 = '/html/body/div[3]/div[2]/div[1]'
                contentXpath3 = '//*[@id="yc_con_txt"]'
                # news_infoXpath = '/html/head/script[6]/text()'

                # 标题
                if article.xpath(titleXpath):
                    news_item = newsItem()# 实例化条目
                    get_title(article, titleXpath, news_item)
                    news_item['url'] = url
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        try:
                            get_content(article, contentXpath, news_item)
                            count += 1
                            news_item['id'] = count
                        except 1:
                            get_content(article, contentXpath2, news_item)
                            count += 1
                            news_item['id'] = count
                        except 2:
                            get_content(article, contentXpath3, news_item)
                            count += 1
                            news_item['id'] = count
                    # 评论
                    try:
                        comment_url = get_comment_url2(article, url)
                        # 评论处理
                        comments = get_comment(comment_url, news_item)[1]
                        news_item['comments'] = comments
                    except:
                        news_item['comments'] = ' '
                        news_item['heat'] = 0
                    yield news_item
'''网站分类函数'''
def get_category(article):
    if article.xpath('//*[@id="artical"]'):
        case = 1#最近的凤凰新闻
        return case
    elif article.xpath('/html/body/div[3]'):
        case = 2 #
        return case
    elif article.xpath('/html/body/div[4]'):
        case = 3
        return case
    # elif article.xpath('/html/body/div[2]'):
    #    case = 4
    #    return case
'''通用标题处理函数'''
def get_title(article, titleXpath, news_item):
    #标题
    try:
        article_title = article.xpath(titleXpath).extract()[0]
        article_title = article_title.replace('\n', ' ')
        article_title = article_title.replace('\r', ' ')
        article_title = article_title.replace('\t', ' ')
        article_title = article_title.replace(' ', '')
        news_item['title'] = article_title
    except:
        news_item['title'] = ' '

'''通用日期处理函数'''
def get_date(article, dateXpath, news_item):
    # 时间
    try:
        article_date = article.xpath(dateXpath).extract()[0]
        pattern = re.compile("(\d.*\d)")  # 正则匹配新闻时间
        article_datetime = pattern.findall(article_date)[0]
        # 替换日期中的汉字
        try:
            article_datetime = article_datetime.replace('年', '-')
            article_datetime = article_datetime.replace('月', '-')
            article_datetime = article_datetime.replace('日', '')
        except:
            pass
        #article_datetime = datetime.datetime.strptime(article_datetime, "%Y-%m-%d %H:%M:%S")
        news_item['date'] = article_datetime
    except:
        news_item['date'] = '2010-10-01 17:00:00'

'''通用正文处理函数'''
def get_content(article, contentXpath, news_item):
    try:
        content_data = article.xpath(contentXpath )
        article_content = content_data.xpath('string(.)').extract()

        article_content = ' '.join(article_content)
        article_content = article_content.replace(' ', '')
        article_content = article_content.replace('\t', '')
        article_content = article_content.replace('\n', '')
        article_content = article_content.replace('\r', '')
        for ch in article_content:
            if (u'\u4e00' <= ch <= u'\u9fff'):
                pass
        news_item['content'] = article_content
        # 匹配新闻简介
        index = article_content.find('。')
        abstract = article_content[0:index]
        news_item['abstract'] = abstract
    except:
        news_item['content'] = ' '
        news_item['abstract'] = ' '

'''评论信息提取函数'''
def get_comment_url(article, url):
    try:
        comment_url = 'http://comment.ifeng.com/get.php?job=1&doc_url=' + url
        return comment_url
    except:
        return
def get_comment_url2(article, news_infoXpath):
    news_info = article.xpath(news_infoXpath)  # 包含评论信息的变量
    news_info_text = news_info.extract()[0]
    pattern = re.compile('"commentUrl":(.*)')  # 正则匹配新闻id
    commentUrl_text = pattern.findall(news_info_text)[0]
    commentUrl  = commentUrl_text.replace('"', '')
    commentUrl = commentUrl.replace(',', '')
    comment_url = 'http://comment.ifeng.com/get.php?job=1&doc_url=' + commentUrl + '&job=1'
    return comment_url

'''评论处理函数'''
def get_comment(comment_url, news_item):
    comments = []
    comment_id = 0
    try:
        comment_data = requests.get(comment_url).text
        js_comment = json.loads(comment_data)
        try:
            heat = js_comment['count']
            news_item['heat'] = heat
            js_comments = js_comment['comments']
            for each in js_comments:
                comment_id += 1
                comments_dict = {}
                # 评论id
                comments_dict['id'] = comment_id
                # 评论用户名
                try:
                    comments_dict['username'] = each['uname']
                except:
                    comments_dict['username'] = '匿名用户'
                # 评论时间，datetime格式
                timestamp = int(each['add_time'])
                timeArray = time.localtime(timestamp)
                date_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                comments_dict['date_time'] = date_time
                # 评论内容
                comments_dict['content'] = each['comment_contents']
                comments.append(comments_dict)
                #a = 1
            return heat, comments
        except:
            return 0, ' '
    except:
        return 0, ' '
