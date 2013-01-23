import json
import datetime
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from vtrScrapy.items import Schedule,Program
from scrapy import log
from datetime import date

class FichaSpider(BaseSpider):
    name = "fichas"


    def __init__(self):
        self.start_urls=['http://televisionvtr.cl/pel%C3%ADculas/men-in-black/']


    def parse(self, response):
        prog = response.meta['prog']
        hxs = HtmlXPathSelector(response)
        ficha = hxs.select('//div[@id="ficha"]')
        info = ficha.select('div/div[@class="info"]')
        keys = info.select('strong/text()').extract()
        values = info.select('span/text()').extract()

        program = Program()
        program['photo']  = ficha.select('div[@class="imagen"]/img/@src').extract()[0]
        program['name'] = info.select('h2/text()').extract()[0]
        program['description'] = info.select('p/text()').extract()[0]


        for k,v in zip (keys,values):
            if( k == u'G\xe9nero:'):
                program['genre']={'name':v}
            elif( k == u'Protagonistas:'):
                program['actors'] = {'name':v}
            elif( k == u'Director:' ):
                program['director'] = {'name':v}
            elif( k == u'Calificaci\xf3n:'):
                program['certification'] = v
            elif( k == u'Web oficial:'):
                program['web'] = v
            else:
                log.msg('key "%s" with value "%s" cannot calificate' % (k,v), log.WARNING)
        program['_id'] = prog
        # horarios= hxs.select('//div[@id="horario"]/table/tbody/tr')
        # items = []
        # for horario in horarios:
        #     item = Schedule()
        #     startTime=  horario.select('td[@class="hora"]/text()').extract()[0]
        #     startDate = horario.select('td[@class="horario_dia"]/strong/text()').extract()[0]
        #     item['start'] = datetime.datetime.strptime(startDate+startTime[:-12],'%d/%m/%Y%H:%M hrs')
        #     items.append(item)
        # program['schedules'] = items
        return program

