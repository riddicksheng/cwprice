# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CwpriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #产品分类
    tag = scrapy.Field()
    #产品名称
    product_name = scrapy.Field()
    #产品ID
    product_id = scrapy.Field()
    #产品价格
    price = scrapy.Field()
    #节省费用
    savings = scrapy.Field()
    #零售价
    retail_price = scrapy.Field()
    #到货时间
    shipping_time_indicator = scrapy.Field()
    #缺货时描述
    outOfStock_abs = scrapy.Field()
    #产品图片url地址
    front_image_url = scrapy.Field()
    #产品图片的本地地址
    front_image_path = scrapy.Field()
    #当前url
    url = scrapy.Field()
    #对当前url进行md5转换，作为主键
    url_object = scrapy.Field()
    #主键，product_id+url+crwal_time组成，用于区分不同时间抓取的数据
    index_no = scrapy.Field()
    #抓取时间
    crawl_time = scrapy.Field()

