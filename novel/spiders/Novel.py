# -*- coding: utf-8 -*-
import scrapy
from novel.items import NovelItem
from novel import c2n
import env


class NovelSpider(scrapy.Spider):
    name = 'Novel'
    allowed_domains = env.allowed_domains
    start_urls = env.start_url
    base_url = env.base_url

    def parse(self, response):
        slist = response.xpath("/html/body/div[2]/div[5]/span/a/@href").extract()
        for i in slist:
            #print(self.base_url + i)
            yield scrapy.Request(self.base_url + i ,callback=self.get_content)

    def get_content(self, response):
        item = NovelItem()
        title = response.xpath("/html/body/div[2]/h1/text()").extract()[0]
        title = title.replace("章节目录 ", "")
        content = response.xpath("//*[@id='content']/text()").extract()
        content = "".join(content)
        replace_list = env.replace_list
        for rep in replace_list:
            content = content.replace(rep,"")
        item['title'] = title
        item['content'] = content
        item['tid'] = c2n.Cn2An(c2n.get_tit_num(title))
        return item
