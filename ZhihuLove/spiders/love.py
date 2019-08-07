# -*- coding: utf-8 -*-
import scrapy
from ZhihuLove.items import ZhihuloveItem

'''

    爬虫关键部分
    创建于 2019/7/1
    实验性的爬取数据
    爬取知乎相亲的数据 获取数据下来不做数据分析
    Scrapy 爬虫爬取知乎数据
    开始执行数据的时候
    
'''

# 全局的获取数据从第一行开始
ct = 0


class LoveSpider(scrapy.Spider):
    name = 'love'
    allowed_domains = ['www.zhihu.com']

    # 择偶标准的查询
    start_urls = ['https://www.zhihu.com/question/275359100/answers/updated/']

    def parse(self, response):
        # 获取总的问题节点
        question = response.xpath('//div[@class="Question-main"]')

        infos = question.xpath('./div//div[@class="List-item"]')

        allStr = ""

        if infos and len(infos):

            item = ZhihuloveItem()

            info = infos[0]

            count = info.xpath('./div[@class="ContentItem AnswerItem"]')

            username = count.xpath('//div[@class="Popover"]/div/a[@class="UserLink-link"]/text()').extract()

            if username and len(username):
                item['username'] = username[0]
            else:
                item['username'] = '匿名用户'

            introduce = count.xpath('//div[@class="ztext AuthorInfo-badgeText"]/text()').extract()

            if introduce and len(introduce):
                item['introduce'] = introduce[0]
            else:
                item['introduce'] = '这个人太懒啥也没有留下'

            cons = count.xpath('//div[@class="RichContent-inner"]'
                               '/span[@class="RichText ztext CopyrightRichText-richText"]'
                               '//p//text()').extract()
            for ok in cons:
                allStr += ok

            item['content'] = allStr

            yield item

        # 定义从第一条数据开始执行
        global ct

        # 下一页数据
        new_pages = infos.xpath('//div[@class="Pagination"]/'
                                'button[@class="Button PaginationButton Button--plain"]/text()').extract()
        if new_pages and len(new_pages):
            sk = new_pages[len(new_pages) - 1]
            sq = int(sk)
            if ct < sq:
                ct += 1
                new_page = "page=" + str(ct)
                yield scrapy.Request("https://www.zhihu.com/question/275359100/answers/updated?"
                                     + new_page, callback=self.parse)
