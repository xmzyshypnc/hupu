#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import chardet
import pymysql

class HupuPipeline(object):

    page_num = 0

    def process_item(self, item, spider):
        title = item['title']
        author = item['author']
        date = item['date']
        content = item['content'].decode('utf-8')
        #
        # print(type(title))
        #
        # print chardet.detect(title)
        # print chardet.detect(author)
        # print chardet.detect(date)
        # print chardet.detect(content)


        # 和本地的newsDB数据库建立连接
        db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='amazing12138*',  # 自己的密码
            db='hupu',  # 数据库的名字
            charset='utf8mb4',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)
        # if db:
        #     print ('success')
        # else:
        #     print ('failed to connect')
        try:
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 插入语句
            #print('123456')
            #sql = "INSERT INTO hupu(title,author,date, content) VALUES ('%s', '%s', '%s', '%s')" % (title, author, date, content)
            self.page_num += 1
            sql = "INSERT INTO hupu(page_num, title,author,date_time, content) VALUES ('%s', '%s', '%s', '%s', '%s')" % (self.page_num, title, author, date, content)
            #print sql
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        finally:
            # 关闭连接
            db.close()
        return item



