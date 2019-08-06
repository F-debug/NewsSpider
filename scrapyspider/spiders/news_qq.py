# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from ..items import newsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re, requests
import json

count = 49687

class NewsqqSpider(CrawlSpider):

    # 爬虫名称
    name = "qqnews"
    # 伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    #网易全网
    allowed_domains = [
        "qq.com"
    ]
    #新闻版
    start_urls = [
        "http://news.qq.com/"
    ]
    #可以继续访问的url规则,http://(\a)*.sina.com.cn(/([\w\._+-])*)*$
    rules = [
        Rule(LinkExtractor(allow=('http://news.qq.com/a(/([\w\._+-])*)*$')), callback="parse_item", follow=True),
    ]
    def parse_item(self, response):
        global count
        # response是当前url的响应
        article = Selector(response)
        url = response.url


        # 分析网页类型
        if get_category(article) == 1:
            titleXpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()'
            dateXpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[3]/text()'
            contentXpath = '//*[@id="Cnt-Main-Article-QQ"]'
            news_infoXpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[2]/script/text()'
            # 标题

            if article.xpath(titleXpath):
                news_item = newsItem()
                get_title(article, titleXpath, news_item)
                news_item['url'] = url
                # 日期
                if article.xpath(dateXpath):
                    get_date(article, dateXpath, news_item)
                # 内容
                try:
                    get_content(article, contentXpath, news_item)
                    count += 1
                    news_item['id'] = count
                except:
                    return
                # 评论
                # try:
                #     comment_url = get_comment_url(article, news_infoXpath)
                #     # 评论处理
                #     comments = get_comment(comment_url, news_item)[1]
                #     news_item['comments'] = comments
                # except:
                news_item['comments'] = ' '
                news_item['heat'] = 0
                yield news_item


'''网站分类函数'''
def get_category(article):
    try:
        article.xpath('/html/body/div[3]/div[1]/div[1]')
        case = 1
        return case
    except:
        return 0


'''通用标题处理函数'''
def get_title(article, titleXpath, news_item):
    #标题
    article_title = article.xpath(titleXpath).extract()[0]
    article_title = article_title.replace('\n', '')
    article_title = article_title.replace('\r', '')
    article_title = article_title.replace('\t', '')
    article_title = article_title.replace(' ', '')
    news_item['title'] = article_title



'''通用日期处理函数'''
def get_date(article, dateXpath, news_item):
    # 时间
    try:
        article_date = article.xpath(dateXpath).extract()[0]
        pattern = re.compile("(\d.*\d)")  # 正则匹配新闻时间
        article_datetime = pattern.findall(article_date)[0]
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
        article_content = article_content.replace('\n', ' ')
        article_content = article_content.replace('\t', ' ')
        article_content = article_content.replace('\r', ' ')
        article_content = article_content.replace('  ', ' ')
        news_item['content'] = article_content
        # 匹配新闻简介
        index = article_content.find('。')
        abstract = article_content[0:index]
        news_item['abstract'] = abstract
    except:
        news_item['content'] = ' '
        news_item['abstract'] = ' '

'''评论信息提取函数'''
def get_comment_url(article, news_infoXpath):
    news_info = article.xpath(news_infoXpath)
    news_info_text = news_info.extract()[0]
    pattern = re.compile("cmt_id = (.*);")
    news_id_text = pattern.findall(news_info_text)[0]
    # news_id = re.findall(r"(\d.*)", news_id_text)
    comment_url = 'http://coral.qq.com/article/'+ news_id_text+'/comment/v2?'
    return comment_url

'''评论处理函数'''
def get_comment(comment_url, news_item):
    comments = []
    comment_id = 0
    try:
        comment_data = requests.get(comment_url).text
        js_comment = json.loads(comment_data)
        try:
            jsObj = js_comment['jsonObject']
            heat = jsObj['participation_sum']
            news_item['heat'] = heat
            comments = jsObj['comments']
            return heat, comments
        except:
            return 0, ' '
    except:
        return 0, ' '
