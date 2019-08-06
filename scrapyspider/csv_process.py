#用于将新闻中的评论内容单独存表
# -*- coding:utf-8 -*-
import csv, re
import pandas
import sys
maxInt = sys.maxsize
decrement = True


# 爬取的新闻csv文件
csv_path = 'E:\Python\以前的项目\\NewsSpider-master\\网易新闻0831.csv'
# 评论文件输出路径
out_path = 'E:\Python\以前的项目/NewsSpider-master\网易新闻0831评论.csv'

# 将爬取的新闻内容保存到csv文件
def csv_process():
    id = []
    username = []
    date_time = []
    content = []
    news_id = []

    # 这里指定csv文件的保存路径
    news_dict = csv.reader(open(csv_path, encoding='ANSI'))
    count = 0
    for items in news_dict:
        try:
            newsid = items[5]
            comment_data = items[1]
            keyword_start =u'{'
            keyword_end = u'}'

            #寻找每条评论的起止位置
            comment_start = [m.start() for m in re.finditer(keyword_start, comment_data)]
            comment_end = [n.start() for n in re.finditer(keyword_end, comment_data)]

            # 提取每条评论
            for i in range(0,len(comment_end)):
                comments = comment_data[comment_start[i]:comment_end[i]]
                id_start = comments.find("'id':")
                id_end = comments.find(", 'username'")
                id.append(comments[id_start + 5 : id_end])

                username_start = comments.find("'username':")
                username_end = comments.find(", 'date_time'")
                username.append(comments[username_start + 13 : username_end-1])

                datetime_start = comments.find("'date_time':")
                datetime_end = comments.find(", 'content'")
                date_time.append(comments[datetime_start + 14 : datetime_end-1])

                content_start = comments.find("'content':")
                content_end = comments.find("}]")
                content.append(comments[content_start + 12: content_end])

                news_id.append(newsid)
            count += 1
        except:
            continue

    #字典中的key值即为csv中列名
    dataframe = pandas.DataFrame(
        {'id':id,
         'username':username,
         'date_time':date_time,
         'content':content,
         'news_id':news_id}
    )

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv(
        out_path,
        index=False,
        encoding='utf_8_sig'
    )

while decrement:
    # 每当出现OverflowError就将maxInt减小10倍
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt / 10)
        decrement = True
csv_process()
