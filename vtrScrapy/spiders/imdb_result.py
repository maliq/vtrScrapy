import json
import datetime
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy import log
from datetime import date

class ImdbResult(Item):
    url = Field()
    imdbId = Field()
    title = Field()
    postTitle = Field()
    selected =Field()

class ImdbSpider(Spider):
    name = "imdb"

    def __init__(self,key):
        self.start_urls=['http://www.imdb.com/find?q=%s&s=tt' % key]

    def parse(self, response):
        hxs = Selector(response)
        results = hxs.xpath('//table[@class="findList"]/tr/td[@class="result_text"]')
        urls=[]
        for result in results:
            r=ImdbResult()
            r['url'] = result.xpath('a/@href').extract()[0]
            r['title'] = result.xpath('a/text()').extract()[0]
            r['imdbId'] = r['url'][9:16]
            yt = result.xpath('text()').extract()[1]
            r['postTitle'] = yt
            urls.append(r)
            log.msg('url: %s found' % r['url'] ,log.INFO)
        log.msg('{0} results found'.format(len(urls)),log.INFO)
        return urls
