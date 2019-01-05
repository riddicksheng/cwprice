# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from cwprice.items import CwpriceItem
from cwprice.utils.common import get_md5
import datetime

"""
2018-12-5：
1、allowed_domains影响，不能进行进一步解析，待解决
"""



class CwpriceSpider(scrapy.Spider):
    name = 'cwprice'
    allowed_domains = ['chemistwarehouse.com.au']
    # start_urls = ['https://www.chemistwarehouse.com.au/shop-online/81/vitamins/']
    start_urls = ['https://www.chemistwarehouse.com.au/']

    def parse(self, response):


        """
        1、获取文章列表页中的文章url并交给csrapy下载并进行解析
        2、获取到下一页的url并交给scrapy进行下载，下载完成后交给parse
        """

        menu_nodes = response.css("#HomeMenu nav.desktop-only-container li a::attr(href)").extract()
        menu_nodes.remove("/prescriptions")
        menu_nodes.remove("/bestsellers")
        menu_nodes.remove("/categories")
        for menu_node in menu_nodes:
            yield Request(url=parse.urljoin(response.url, menu_node), callback=self.parse_menu)
            # print(menu_node)

    def parse_menu(self, response):

        #解析当前页列表中所有文章的url并交给scrapy下载，并进行解析
        post_nodes = response.css(".product-list-container a")
        for post_node in post_nodes:
            image_url = post_node.css(".product-image img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            #parse.urljoun()实现当前域名与获取url的拼接
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url},  callback=self.parse_detail)
            # yield Request(url=parse.urljoin(response.url, post_url),  callback=self.parse_detail)
            # print(post_url)

        #获取当前也的下一页链接
        next_url = response.css("a.next-page::attr(href)").extract_first()
        print(next_url)
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse_menu)

    def parse_detail(self, response):

        cwprice_item = CwpriceItem()

        #产品分类
        tag_list = response.css("div.breadcrumbs a::text").extract()
        tag_list = [element.strip() for element in tag_list]
        tag = "/".join(tag_list)

        #产品名称
        product_name = response.css("div.product-name h1::text").extract_first()
        if product_name:
            product_name = product_name.strip()

        #产品ID
        product_id = response.css(".product-id::text").extract_first()
        re_match = re.match(".*?(\d+).*", product_id)
        if re_match:
            product_id = re_match.group(1)
        else:
            product_id = "NONE"

        #产品价格
        price = response.css("div.Price span::text").extract_first().strip("$")

        #节省费用
        savings = response.css("div.Savings::text").extract_first()
        re_match = re.match(".*?(\d+.\d+).*", savings)
        if re_match:
            savings = float(re_match.group(1))
        else:
            savings = 0

        #零售价
        retail_price = response.css("div.retailPrice::text").extract_first().strip()
        re_match = re.match(".*?(\d+.\d+).*", retail_price)
        if re_match:
            retail_price = float(re_match.group(1))
        else:
            retail_price = 0

        #到货时间
        shipping_time_indicator = response.css("div.shipping_time_indicator[style='display:block'] span::text").extract_first()
        # if not shipping_time_indicator :
        #     shipping_time_indicator = "现货"

        #缺货时描述
        outOfStock_abs = response.css("div[style='display:block'] div.Add2Cart[style*='block'] div::text").extract()
        outOfStock_abs = ''.join(outOfStock_abs)

        #获取封面图片
        front_image_url = response.meta.get("front_image_url")

        #抓取时间
        crawl_time = datetime.datetime.now().date()

        cwprice_item["tag"] = tag
        cwprice_item["product_name"] = product_name
        cwprice_item["product_id"] = product_id
        cwprice_item["price"] = price
        cwprice_item["savings"] = savings
        cwprice_item["retail_price"] = retail_price
        cwprice_item["shipping_time_indicator"] = shipping_time_indicator
        cwprice_item["outOfStock_abs"] = outOfStock_abs
        cwprice_item["front_image_url"] = [front_image_url]
        cwprice_item["url"] = response.url
        cwprice_item["url_object"] = get_md5(response.url)
        cwprice_item["crawl_time"] = crawl_time
        cwprice_item["index_no"] = get_md5(product_id+response.url+str(crawl_time))

        yield cwprice_item


