# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class CwpricePipeline(object):
    def process_item(self, item, spider):
        return item


class CwproductImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        print("image_file_path :", image_file_path)
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        insert_sql = """
            insert into cwprice (index_no, tag, product_name, product_id, price, savings, retail_price, shipping_time_indicator,
                       outOfStock_abs, front_image_url, front_image_path, url, url_object,crawl_time)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["index_no"], item["tag"], item["product_name"], item["product_id"], item["price"],
                                    item["savings"],item["retail_price"], item["shipping_time_indicator"],
                                    item["outOfStock_abs"],item["front_image_url"], item["front_image_path"], item["url"],
                                    item["url_object"], item["crawl_time"]))
