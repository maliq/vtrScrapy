import json
from scrapy.spider import Spider
from scrapy.selector import Selector
from vtrScrapy.items import Schedule,Channel
from scrapy import log

class CanalesSpider(Spider):
	name = "channels"
	channelTypeList = ['series-peliculas', 'deportes','infantil','musica','tendencias','cultura','noticias','internacional','adulto','premium','hd']

	def __init__(self, comuna='Valparaiso'):
		# self.start_urls = ['http://televisionvtr.cl/index.php?obt=grilla&comuna=Santiago&canal_inicio=1&canal_cantidad=%s' % top]
		self.comuna = unicode(comuna)
		self.start_urls = []
		for channelType in self.channelTypeList:
			self.start_urls.append( 'http://televisionvtr.cl/index.php?obt=grilla&canal_tipo=%s&comuna=%s' % (channelType,comuna))

	def parse(self, response):
		# filename = response.url.split("/")[-2]
		# open(filename, 'wb').write(response.body)
		jdata=json.loads(response.body)
		channelType = unicode(response.url.split("&")[1].replace('canal_tipo=',''))
		# print jdata['canales']
		hxs = Selector(text=jdata['canales'])
		channels = hxs.xpath('//li')
		items = []
		for chan in channels:
			channel = Channel()
			channel['cod'] = chan.xpath('@id').extract()[0]
			channel['name'] = chan.xpath('img/@alt').extract()[0]
			channel['logo'] = chan.xpath('img/@src').extract()[0]
			channel['description'] = chan.xpath('img/@title').extract()[0]
			channel['numbers'] = [{self.comuna : chan.xpath('div/strong/text()').extract()[0]}]
			channel['type'] = channelType
			items.append(channel)
		log.msg('{0} channels found'.format(len(items)),log.INFO)
		return items
