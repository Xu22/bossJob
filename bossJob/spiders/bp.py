# -*- coding: utf-8 -*-
import scrapy
from bossJob.items import BossjobItem
import time
from scrapy.http import Request
class BpSpider(scrapy.Spider):
    name = 'bp'
    allowed_domains = ['www.zhipin.com']
    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
    }
    start_urls = [
        'https://www.zhipin.com/'
    ]
    curPage=1
    url='https://www.zhipin.com/c101020100-p100109/'
    def start_requests(self):
        return [self.next_request()]
    def parse(self, response):
        item=BossjobItem()
        selector=scrapy.Selector(response)
        jobs=selector.xpath('//div[@class="job-primary"]')
        for job in jobs:
            item['jobTitle'] =job.xpath('.//div[@class="job-title"]/text()').extract()[0].strip()
            item['jobSalary'] = job.xpath('.//span[@class="red"]/text()').extract()[0].strip()
            item['jobCompany'] = job.xpath('.//div[@class="company-text"]/h3[@class="name"]/a/text()').extract()[0].strip()
            item['jobPublish'] = job.xpath('.//div[@class="info-publis"]/p/text()').extract()[0].strip()
            yield item
        next_page = selector.xpath('//a[@class="next"]/@href').extract()

        if next_page:
            self.curPage+=1
            time.sleep(5)
            yield self.next_request()
    def next_request(self):
        return scrapy.Request(self.url+("?page=%d&ka=page-%d"%(self.curPage,self.curPage)), callback=self.parse,headers=self.headers, dont_filter=False)
