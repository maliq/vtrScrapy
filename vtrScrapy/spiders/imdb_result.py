import json
import datetime
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy import log
from datetime import date

class ImdbResult(Item):
    url = Field()

class ImdbSpider(BaseSpider):
    name = "imdb"


    def __init__(self,key):
        # conn= Connection()
        # db = conn.vtr
        # programs= db.programs

        self.start_urls=['http://www.imdb.com/find?q=%s&s=tt' % key]
        self.items = []

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//table[@class="findList"]/tr/td[@class="result_text"]/a')
        for result in results:
            r=ImdbResult()
            r['url'] = result.select('@href').extract()[0]
            self.items.append(r)
            log.msg('url: %s found' % r['url'] ,log.INFO)
        log.msg('{0} results found'.format(len(self.items)),log.INFO)
        return self.items

    def items(self):
        self.items
