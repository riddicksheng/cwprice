# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class FirstspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
            print(ok)
        item["front_image_path"] = image_file_path

        return item


class MysqlPipeline(object):
    def __init__(self):
        # host = 'localhost'
        # user = 'root'
        # password = 'xxltony13'
        # dbname = 'test'
        # self.conn = MySQLdb.connect(host, user, password, dbname, charset='utf8', user_unicode=True)
        self.conn = MySQLdb.connect('localhost', 'root', 'xxltony13', 'test', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article ( url_object, title, url, create_date, fav_num)
            VALUES(%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["url_object_id"], item["title"], item["url"], item["create_date"], item["fav_num"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return  cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        insert_sql = """
            insert into article ( url_object, title, url, create_date, fav_num)
            VALUES(%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["url_object_id"], item["title"], item["url"], item["create_date"], item["fav_num"]))
