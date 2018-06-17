# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import requests as rsq

class NovelPipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        tid = item['tid']
        name = 'novel'
        connection = pymysql.connect(
            host='bwg.kidding.men',  # 连接的是本地数据库
            port=3306,
            user='winfath',  # 自己的mysql用户名
            passwd='winfath0215',  # 自己的密码
            db='books',  # 数据库的名字
            charset='utf8mb4',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # 数据库表的sql
                # 单章小说的写入
                sql = 'Insert into %s values ("%d","%s","%s")' % (name,int(tid), title, content)
                cursor.execute(sql)

            # 提交本次插入的记录
            connection.commit()
            print('-------------------')
        finally:
            # 关闭连接
            connection.close()
            return item
        # esUrl = "http://45.32.254.237:9200/books/novel"
        # headers = {'Content-Type': 'application/json'}
        # params = {
        #     "tid":tid,
        #     "title":title,
        #     "content":content
        # }
        # rsq.post(esUrl,data=params,headers=headers)