import json
import datetime
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from vtrScrapy.items import Schedule,Program
from scrapy import log
from datetime import date

class MinifichaSpider(BaseSpider):
    name = "minificha"

    def __init__(self):
        self.start_urls=['http://televisionvtr.cl/index.php?obt=minificha&channels=518977423&programs=335592&starttime=0505&startdate=010913&canal_tipo=peliculas']

    def parse(self, response):
        prog = response.meta['prog']
        hxs = HtmlXPathSelector(response)
        ficha = hxs.select('//div[@id="ficha"]')
        info = ficha.select('div/div[@class="text"]')
        title = info.select('strong/text()').extract()[0]
        descriptions = info.select('p/text()').extract()
        program = Program()
        for des in descriptions:
            if 'Actores: ' in des :
                program['actors'] = {'name':des.replace('Actores: ','')}
            elif 'Director:' in des :
                program['director'] = {'name':des.replace('Director: ','')}
            elif 'Episodio: ' in des :
                program['episode'] = des.replace('Episodio: ','')
            else:
                program['description'] = des
        program['name']= title
        program['_id'] = prog
        return program

