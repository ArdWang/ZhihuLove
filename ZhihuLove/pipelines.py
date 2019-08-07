# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors


class ZhihulovePipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='zhihu_db',
            user='root',
            passwd='5324840',
            charset='utf8',
            use_unicode=True
        )
        self.cursors = self.connect.cursor()

    # 重写close_spider回调方法，用于关闭数据库资源
    def close_spider(self, spider):
        print('----------关闭数据库资源-----------')
        # 关闭游标
        self.cursors.close()
        # 关闭连接
        self.conn.close()

    def process_item(self, item, spider):
        self.cursors.execute("insert into love_tb(username,introduce,content)value(%s,%s,%s)",
                             (item['username'], item['introduce'], item['content']))
        self.connect.commit()
        return item
