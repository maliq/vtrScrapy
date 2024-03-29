import json
import datetime
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from vtrScrapy.items import Schedule,Program
from scrapy import log
from datetime import date
from bson.objectid import ObjectId
from vtrScrapy.spiders.channels_spider import CanalesSpider

class ScheduleSpider(Spider):
    name = "schedule"

    def __init__(self, gap=10, top=147,comuna='Valparaiso', channelType = '', **kwargs):
        gap=int(gap)
        top=int(top)
        gap = gap if gap<top else top
        today=date.today()
        date_str=today.strftime("%m%d%y")
        # date_str='{0:02d}{1:02d}{2}'.format(today.month,today.day,str(today.year)[2:])
        self.start_urls=[]
        for start in range(1,top,gap):
            for channelTypeItem in CanalesSpider.channelTypeList:
                if channelType == '':
                    self.start_urls.append('http://televisionvtr.cl/index.php?obt=grilla&comuna={0}&canal_inicio={1}&canal_cantidad={2}&canal_tipo={3}&fecha={4}'.\
                    format(comuna,str(start),str(start+gap-1),channelTypeItem,date_str))
                elif channelType == channelTypeItem:
                    self.start_urls.append('http://televisionvtr.cl/index.php?obt=grilla&comuna={0}&canal_inicio={1}&canal_cantidad={2}&canal_tipo={3}&fecha={4}'.\
                    format(comuna,str(start),str(start+gap-1),channelType,date_str))


    def parse(self, response):
        jdata=json.loads(response.body)
        hxs = Selector(text=jdata['grilla'])
        channels = hxs.xpath('//ul')
        hxsChan = Selector(text=jdata['canales'])
        channelNames = hxsChan.xpath('//li/img/@alt').extract()

        items = []
        for channel,chanName in zip(channels,channelNames):
            channelType=channel.xpath('@class').extract()[0].split(' ')[2]
            sites = channel.xpath('li')
            for site in sites:
                schedule = Schedule()
                startTime= site.xpath('@data-starttime').extract()[0]
                startDate = site.xpath('@data-startdate').extract()[0]
                chan=site.xpath('@data-chn').extract()[0]
                prog=site.xpath('@data-prog').extract()[0]
                schedule['start'] = datetime.datetime.strptime(startDate+startTime,"%m%d%y%H%M")
                duration=site.xpath('@data-duration').extract()[0]
                schedule['duration'] = int(duration[2:])+int(duration[:2])*60
                schedule['chn'] = {'cod':chan,'name':chanName}
                schedule['prog'] = {'cod':prog,'name':site.xpath('a/text()').extract()[0]}
                href = site.xpath('a/@href').extract()[0]
                if  href != '#':
                    schedule['ficha'] = 'http://televisionvtr.cl%s' % href
                    request = Request(schedule['ficha'],callback=self.parseFicha)
                    request.meta['prog'] = prog
                    items.append(request)
                else:
                    schedule['minificha'] = 'http://televisionvtr.cl/index.php?obt=minificha&channels=%s&programs=%s&starttime=%s&startdate=%s&canal_tipo=%s' \
                        % ( chan, prog ,startTime,startDate,channelType)
                    request = Request(schedule['minificha'],callback=self.parseMini)
                    request.meta['prog'] = prog
                    items.append(request)
                items.append(schedule)
        return items

    def parseMini(self, response):
        prog = response.meta['prog']
        hxs = Selector(response)
        ficha = hxs.xpath('//div[@id="ficha"]')
        info = ficha.xpath('div/div[@class="text"]')
        title = info.xpath('strong/text()').extract()[0]
        descriptions = info.xpath('p/text()').extract()
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
        program['cod'] = prog
        return program

    def parseFicha(self, response):
        prog = response.meta['prog']
        hxs = Selector(response)
        ficha = hxs.xpath('//div[@id="ficha"]')
        info = ficha.xpath('div/div[@class="info"]')
        keys = info.xpath('strong/text()').extract()
        values = info.xpath('span/text()').extract()

        program = Program()
        program['photo']  = ficha.xpath('div[@class="imagen"]/img/@src').extract()[0]
        program['name'] = info.xpath('h2/text()').extract()[0]
        program['description'] = info.xpath('p/text()').extract()[0]


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
        program['cod'] = prog
        # horarios= hxs.xpath('//div[@id="horario"]/table/tbody/tr')
        # items = []
        # for horario in horarios:
        #     item = Schedule()
        #     startTime=  horario.xpath('td[@class="hora"]/text()').extract()[0]
        #     startDate = horario.xpath('td[@class="horario_dia"]/strong/text()').extract()[0]
        #     item['start'] = datetime.datetime.strptime(startDate+startTime[:-12],'%d/%m/%Y%H:%M hrs')
        #     items.append(item)
        # program['schedules'] = items
        return program
