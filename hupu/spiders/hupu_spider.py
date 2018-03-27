# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from hupu.items import HupuItem
#from requests import Request
import scrapy
#from requests import *

class HupuSpiser(Spider):
    name = 'hupu_spider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
    }
    url = "https://bbs.hupu.com/bxj"
    start_urls = ["https://bbs.hupu.com/bxj"]
    page_num = 0


    # def start_request(self):
    #     url = "https://bbs.hupu.com/bxj"
    #     yield scrapy.Request(url,headers=self.headers)

    def parse(self,response):
        #命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        #print("1234")
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        articles = response.xpath('//ul[@class="for-list"]/li')
        #print (articles)
        for article in articles:
            # #str = unicode(str, errors='ignore')
            # title = article.xpath('.//div[@class="titlelink box"]/a[@class="truetit"]/text()')
            # if title:
            #
            #     item['title'] = title.extract()[0].encode('utf-8')
            #     #print(item['title'])
            #
            # author = article.xpath('.//div[@class="author box"]/a[@class="aulink"]/text()')
            # if author:
            #     item['author'] = author.extract()[0].encode('utf-8')
            # #print(item['author'])
            # date = article.xpath('.//div[@class="author box"]/a[2]/text()')
            # if date:
            #     item['date'] = date.extract()[0].encode('utf-8')
            urls = article.xpath('.//div[@class="titlelink box"]/a[@class="truetit"]/@href').extract()
            #print(urls)
            for url in urls:
                yield scrapy.Request("https://bbs.hupu.com/" + url, callback=self.parse_item)
            self.page_num += 1
            if self.page_num < 100:
                next_url = self.url + "-" + str(self.page_num)
                yield  scrapy.Request(next_url, callback=self.parse, dont_filter=True)


    def parse_item(self,response):
        item = HupuItem()
        title = response.xpath('//div[@class="bbs-hd-h1"]/h1/text()').extract()[0]
        item['title'] = title
        #print(title)
        author = response.xpath('//div[@id="tpc"]//div[@class="author"]/div[@class="left"]/a[@class="u"]/text()').extract()[0]
        item['author'] = author
        #print(author)
        date = response.xpath('//div[@id="tpc"]//div[@class="author"]/div[@class="left"]/span[@class="stime"]/text()').extract()[0]
        item['date'] = date
        #print(date)
        #contents = response.xpath('// *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2]').extract()
        part_texts = response.xpath('// *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / text()').extract()
        part_divs = response.xpath('// *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / div / text()').extract()
        paragraph_parts = response.xpath('// *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p /text()').extract()
        temp = ""
        if part_texts:
            for part_text in part_texts:
                #part_text = etree.fromstring(part_text)
                #print part_text
                temp += str(part_text.encode('utf-8'))

        if part_divs:
            for part_div in part_divs:
                #part_div = etree.fromstring(part_div)
                #print part_div
                temp += str(part_div.encode('utf-8'))

        if paragraph_parts:
            for paragraph_part in paragraph_parts:
                #paragraph_part = etree.fromstring(paragraph_part)
                #print paragraph_part
                temp += str(paragraph_part.encode('utf-8'))
        # filename = 'result'
        # with open(filename, 'w') as f:
        #     f.writelines("646546")
        #     f.writelines('title:'+title+';'+'author:'+author+';'+'date:'+date+';'+'content:'+temp+';')

        # for content in contents:
        #     temp += content
        item['content'] = temp
        #print(temp)


        yield item
    #        // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[7] / text()
            # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[5] / img
    #         // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / text()
    #
    #         // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / text()
    #         // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / div[1]
    #
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[1]
    #
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / div[2]
    #
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / div[7]
    #
    #
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[1] / text()
    #
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[2] / text()
    #
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[3] / img
    # // *[ @ id = "tpc"] / div / div[2] / table[1] / tbody / tr / td / div[2] / p[3] / a