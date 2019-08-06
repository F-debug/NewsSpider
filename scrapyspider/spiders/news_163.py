# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from ..items import newsItem
from scrapy.linkextractors import LinkExtractor
import re, requests, json
from scrapy.selector import Selector
count = 0

class news163_Spider(CrawlSpider):
    # 网易新闻爬虫名称
    name = "163news"
    # 伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    #网易全网
    allowed_domains = [
        "163.com"
    ]
    #新闻版
    start_urls = [
        'http://news.163.com/'
    ]
    #可以继续访问的url规则,http://news.163.com/\d\d\d\d\d(/([\w\._+-])*)*$
    rules = [
        Rule(LinkExtractor(
        allow=(
            ('http://news\.163\.com/.*$')
            # ('http://ent\.163\.com/.*$'),
            # ('http://money\.163\.com/.*$'),
            # ('http://war\.163\.com/.*$'),
            # ('http://sport\.163\.com/.*$'),
            # ('http://tech\.163\.com/.*$'),
            # ('http://fashion\.163\.com/.*$'),
            # ('http://auto\.163\.com/.*$'),
            # ('http://jiankang\.163\.com/.*$')
        ),
        deny = ('http://.*.163.com/photo.*$')
        ),
        callback="parse_item",
        follow=True)
    ]
    def parse_item(self, response):
        # response是当前url的响应
        article = Selector(response)
        article_url = response.url
        global count
        # 分析网页类型
        # 比较新的网易新闻 http://news.163.com/05-17/
        if get_category(article) == 1:
            articleXpath = '//*[@id="epContentLeft"]'
            if article.xpath(articleXpath):
                titleXpath = '//*[@id="epContentLeft"]/h1/text()'
                dateXpath = '//*[@id="epContentLeft"]/div[1]/text()'
                contentXpath = '//*[@id="endText"]'
                news_infoXpath ='//*[@id="post_comment_area"]/script[3]/text()'

                # 标题
                if article.xpath(titleXpath):
                    news_item = newsItem()
                    news_item['url'] = article_url
                    get_title(article, titleXpath, news_item)
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        get_content(article, contentXpath, news_item)
                        count = count + 1
                        news_item['id'] = count
                    # 尝试寻找评论
                    try:
                        comment_url = get_comment_url(article, news_infoXpath)
                        # 评论处理
                        comments = get_comment(comment_url, news_item)[1]
                        news_item['comments'] = comments
                    except:
                        news_item['comments'] = ' '
                        news_item['heat'] = 0
                    yield news_item

        # http://news.163.com/40706/
        if get_category(article) == 2:
            articleXpath = '/html/body/table[9]/tr/td[1]'
            if article.xpath(articleXpath):
                titleXpath = '/html/body/table[9]/tr/td[1]/table[1]/tr[1]/td/text()'
                dateXpath = '/html/body/table[9]/tr/td[1]/table[1]/tr[2]/td[2]/table/tbody/tr[2]/td[1]/text()[1]'
                contentXpath = '//*[@id="content"]'
                news_item = newsItem()
                news_item['url'] = article_url
                # 获取标题
                if article.xpath(titleXpath):
                    get_title(article, titleXpath, news_item)
                    # 获取日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        get_content(article, contentXpath, news_item)
                        count = count + 1
                        news_item['id'] = count
                        news_item['heat'] = 0
                        news_item['comments'] = ' '
                yield news_item

        # http://news.163.com/2004w03/
        if get_category(article) == 3:
            articleXpath = '/html/body/table[7]/tr/td[1]'
            if article.xpath(articleXpath):
                titleXpath = '/html/body/table[7]/tr/td[1]/b/span/text()'
                dateXpath = '//html/body/table[7]/tr/td[1]/table[1]/tr/td[1]/div/span/text()'
                dateXpath2 = '/html/body/table[7]/tr/td[1]/table[1]/tr/td[1]/div/span/text()'
                contentXpath = '/html/body/table[7]/tbody/tr/td[1]/table[1]/tbody/tr[1]/td'
                contentXpath2 = '/html/body/table[7]/tr/td[1]/table[2]/tr[1]/td'
                news_item = newsItem()
                news_item['url'] = article_url
                # 标题
                if article.xpath(titleXpath):
                    get_title(article, titleXpath, news_item)
                    # 日期
                    if article.xpath(dateXpath):
                        get_date(article, dateXpath, news_item)
                    elif article.xpath(dateXpath2):
                        get_date(article, dateXpath2, news_item)
                    # 内容
                    if article.xpath(contentXpath):
                        get_content(article, contentXpath, news_item)
                        count = count + 1
                        news_item['id'] = count
                        news_item['heat'] = 0
                        news_item['comments'] = ' '
                    elif article.xpath(contentXpath2):
                        get_content(article, contentXpath2, news_item)
                        count = count + 1
                        news_item['id'] = count
                        news_item['heat'] = 0
                        news_item['comments'] = ' '
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
    if article.xpath('//*[@id="epContentLeft"]'):
        case = 1  # 最近的网易新闻
        return case

    elif article.xpath('/html/body/table[9]/tr/td[1]'):
        case = 2  # 零几年的网易新闻
        return case
    # elif article.xpath('/html/body/table[7]/tr/td[1]'):
    #     case = 3  # 零几年的网易新闻，5位数字开头的
    #     return case

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
    # 提取新闻评论路径
    news_info = article.xpath(news_infoXpath)
    news_info_text = news_info.extract()[0]
    # 正则寻找
    pattern_productKey = re.compile("\"productKey\" :.*")
    productKey_text = pattern_productKey.findall(news_info_text)[0]
    productKey = re.findall(r"\"productKey\".*\"(.*)\"", productKey_text)
    pattern_docId = re.compile("\"docId\" :.*")
    docId_text = pattern_docId.findall(news_info_text)[0]
    docId = re.findall(r"\"docId\".*\"(.*)\"", docId_text)
    comment_url = 'http://comment.news.163.com/api/v1/products/' + productKey[0] + '/threads/' + docId[0] + '/comments/newList?offset=0'
    return comment_url

'''评论处理函数'''
def get_comment(comment_url, news_item):
    comments = []
    comment_id = 0
    try:
        comment_data = requests.get(comment_url).text
        js_comment = json.loads(comment_data)
        try:
            heat = js_comment['newListSize']
            news_item['heat'] = heat
            js_comments = js_comment['comments']
            for each,value in js_comments.items():
                comment_id += 1
                comments_dict = {}
                # 评论id
                comments_dict['id'] = comment_id
                # 评论用户名
                try:
                    comments_dict['username'] = value['user']['nickname']
                except:
                    comments_dict['username'] = '匿名用户'
                try:
                    # 评论时间，datetime格式
                    date_time = value['createTime']
                    #date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
                    comments_dict['date_time'] = date_time
                except:
                    comments_dict['date_time'] = news_item['date']
                # 评论内容
                ori_content = value['content']
                content = str_replace(ori_content)
                comments_dict['content'] = content
                comments.append(comments_dict)
                if comments:
                    return heat, comments
                else:
                    return 0,''
        except:
            return 0, ''
    except:
        return 0, ''



    
