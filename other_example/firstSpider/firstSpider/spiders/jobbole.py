# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from firstSpider.items import JobboleArticleItem
from firstSpider.utils.common import get_md5
import datetime

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        """
        1、获取文章列表页中的文章url并交给csrapy下载并进行解析
        2、获取到下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        #解析当前页列表中所有文章的url并交给scrapy下载，并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            #parse.urljoun()实现当前域名与获取url的拼接
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url},  callback=self.parse_detail)
            print(post_url)

        #获取当前也的下一页链接
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        print(next_url)
        if next_url :
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):

        article_item = JobboleArticleItem()


        #xpath
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extractfirst()
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().strip("·").strip()
        # fav_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        # mark_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # if mark_num :
        #     mark_num = re.match(".*?(\d+).*", mark_num).group(1)
        # comments_num = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # if comments_num :
        #     comments_num = re.match(".*?(\d+).*", comments_num).group(1)
        # create_name = response.xpath("//div[@class='copyright-area']/a/text()").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tag = ",".join(tag_list)
        #
        # content = response.xpath("//div[@class='entry']").extract()[0]


        #css








        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().strip("·").strip()
        fav_num= response.css(".vote-post-up h10::text").extract()[0]
        mark_num = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", mark_num)
        if match_re :
            mark_num = int(match_re.group(1))
        else:
            mark_num = 0
        comments_num = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comments_num)
        if match_re :
            comments_num = int(match_re.group(1))
        else:
            comments_num = 0

        create_name = response.css("div.copyright-area > a::text").extract()[0]
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tag = ",".join(tag_list)
        front_image_url = response.meta.get("front_image_url")#获取封面图片s
        content = response.css("div.entry").extract()[0]

        article_item["title"] = title
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["fav_num"] = fav_num
        article_item["mark_num"] = mark_num
        article_item["comments_num"] = comments_num
        article_item["create_name"] = create_name
        article_item["tag"] = tag
        article_item["content"] = content
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)#对url进行md5转换
        article_item["front_image_url"] = [front_image_url]
        # article_item["front_image_path"] =

        yield article_item
