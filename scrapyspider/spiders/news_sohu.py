# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from ..items import newsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re, requests, time
import json

count = 50000

class newssohu_Spider(CrawlSpider):
    # 爬虫名称
    name = "sohunews"
    # 伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    #网易全网
    allowed_domains = [
        "sohu.com"
    ]
    #新闻版
    start_urls = [
        "http://news.sohu.com/"
    ]
    #可以继续访问的url规则,http://news.163.com/\d\d\d\d\d(/([\w\._+-])*)*$
    rules = [
        Rule(LinkExtractor(
            allow=('http://www.sohu.com(/([\w\._+-])*)*$')),
            callback="parse_item",
            follow=True)
    ]


    def parse_item(self, response):
        global count
        # response是当前url的响应
        article = Selector(response)
        url = response.url
        # 分析网页类型
        # http://www.sohu.com/a/207094395_162758?_f=index_chan08news_0
        if get_category(article) == 1:
            articleXpath = '//*[@id="article-container"]/div[2]'
            if article.xpath(articleXpath):#如果文章页面存在
                titleXpath = '//*[@id="article-container"]/div[2]/div[1]/div[1]/h1/text()'
                dateXpath = '//*[@id="news-time"]/text()'
                contentXpath = '//*[@id="article-container"]/div[2]/div[1]/article'
                news_infoXpath = '/html/body/script[5]/text()'
                # 实例化条目

                # 标题
                if article.xpath(titleXpath):
                    news_item = newsItem()
                    get_title(article, titleXpath, news_item)
                    news_item['url'] = url
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        get_content(article, contentXpath, news_item)
                        count += 1
                        news_item['id'] = count
                    # 评论
                    try:
                        comment_url = get_comment_url(article, news_infoXpath)
                        # 评论处理
                        comments = get_comment(comment_url, news_item)[1]
                        news_item['comments'] = comments
                    except:
                        news_item['comments'] = ' '
                        news_item['heat'] = 0
                    yield news_item


'''通用标题处理函数'''
def get_title(article, titleXpath, news_item):
    #标题
    try:
        article_title = article.xpath(titleXpath).extract()[0]
        article_title = article_title.replace('\n', '')
        article_title = article_title.replace('\r', '')
        article_title = article_title.replace('\t', '')
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
        #article_datetime = datetime.datetime.strptime(article_datetime, "%Y-%m-%d %H:%M:%S")
        news_item['date'] = article_datetime
    except:
        news_item['date'] = '2010-10-01 17:00:00'

'''网站分类函数'''
def get_category(article):
    try:
        article.xpath('//*[@id="article-container"]/div[2]')
        case = 1 # 国内新闻
        return case
    except:
        return

'''字符过滤函数'''
def str_replace(content):
    # article_content = ' '.join(content)
    # rule = re.compile('\w')
    try:
        article_content = re.sub('[\sa-zA-Z\[\]!/*(^)$%~@#…&￥—+=_<>.{}\'\-:;"‘’|]', '', content)
        return article_content
    except:
        return content

'''通用正文处理函数'''
def get_content(article, contentXpath, news_item):
    try:
        content_data = article.xpath(contentXpath )
        article_content = content_data.xpath('string(.)').extract()[0]
        article_content = str_replace(article_content)
        news_item['content'] = article_content
        # 匹配新闻简介，前100个字
        try:
            abstract = article_content[0:100]
            news_item['abstract'] = abstract
        except 1:
            news_item['abstract'] = article_content
            # except 2:
            #     index = article_content.find('。')
            #     abstract = article_content[0:index]
            #     news_item['abstract'] = abstract
    except:
        news_item['content'] = ' '
        news_item['abstract'] = ' '


'''评论信息提取函数'''
def get_comment_url(article, news_infoXpath):
    news_info = article.xpath(news_infoXpath)#包含评论信息的变量
    news_info_text = news_info.extract()[0]
    pattern = re.compile("news_id:(.*)")#正则匹配新闻id
    news_id_text = pattern.findall(news_info_text)[0]
    news_id = re.findall(r"\"(.*)\"", news_id_text)
    comment_url = 'http://apiv2.sohu.com/api/comment/list?page_size&topic_id=1&source_id=mp_' + news_id[0]
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
            js_comments = jsObj['comments']
            for each in js_comments:
                comment_id += 1
                comments_dict = {}
                #评论id
                comments_dict['id'] = comment_id
                #评论用户名
                comments_dict['username'] = each['passport']['nickname']
                try:
                    #评论时间，datetime格式
                    timestamp = int(each['create_time']/1000)
                    timeArray = time.localtime(timestamp)
                    date_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    comments_dict['date_time'] = date_time
                except:
                    comments_dict['date_time'] = news_item['date']

                # 评论内容
                ori_content = each['content']
                comments_dict['content'] = str_replace(ori_content)
                comments.append(comments_dict)
                if comments:
                    return heat, comments
                else:
                    return 0, ''
        except:
            return 0, ''
    except:
        return 0, ''








