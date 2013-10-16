import json
import datetime
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy import log
from datetime import date

class ImdbResult(Item):
    url = Field()
    imdbId = Field()
    title = Field()
    postTitle = Field()
    selected =Field()

class ImdbSpider(BaseSpider):
    name = "imdb"

    def __init__(self,key):
        self.start_urls=['http://www.imdb.com/find?q=%s&s=tt' % key]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//table[@class="findList"]/tr/td[@class="result_text"]')
        urls=[]
        for result in results:
            r=ImdbResult()
            r['url'] = result.select('a/@href').extract()[0]
            r['title'] = result.select('a/text()').extract()[0]
            r['imdbId'] = r['url'][9:16]
            yt = result.select('text()').extract()[1]
            r['postTitle'] = yt
            urls.append(r)
            log.msg('url: %s found' % r['url'] ,log.INFO)
        log.msg('{0} results found'.format(len(urls)),log.INFO)
        return urls
