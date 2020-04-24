# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp import items

#小程序社区爬取文章
class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r".+article-.+\.html"), callback="parse_item", follow=False)

    )

    def parse_item(self, response):
        item = {}
        title=response.xpath("//h1[@class='ph']/text()").get()
        author_p=response.xpath("//p[@class='authors']")
        author=author_p.xpath(".//a/text()").get()
        pub_time=author_p.xpath(".//span/text()").get()
        article_context=response.xpath("//td[@id='article_content']//text()").getall()
        article_context="".join(article_context).split()
        item=items.WxappItem(title=title,author=author,pub_time=pub_time,article_context=article_context)
        yield item
