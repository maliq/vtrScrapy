import json
import datetime
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy import log
from datetime import date

class ImdbResult(Item):
    url = Field()
    imdbId= Field()

class ImdbSpider(BaseSpider):
    name = "imdb"


    def __init__(self,key):
        self.start_urls=['http://www.imdb.com/find?q=%s&s=tt' % key]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//table[@class="findList"]/tr/td[@class="result_text"]/a')
        urls=[]
        r=ImdbResult()
        for result in results:
            url = result.select('@href').extract()[0]
            urls.append(url)
            log.msg('url: %s found' % url,log.INFO)
        log.msg('{0} results found'.format(len(urls)),log.INFO)
        r['url']=urls
        return r
