import json
from scrapy.spider import Spider
from scrapy.selector import Selector
from vtrScrapy.items import Schedule,Channel
from scrapy import log

class CanalesSpider(Spider):
	name = "channels"

	def __init__(self, comuna='Santiago',channelType='series-peliculas'):
		# self.start_urls = ['http://televisionvtr.cl/index.php?obt=grilla&comuna=Santiago&canal_inicio=1&canal_cantidad=%s' % top]
		self.channelType = unicode(channelType)
		self.start_urls =['http://televisionvtr.cl/index.php?obt=grilla&canal_tipo=%s&comuna=%s' % (channelType,comuna)]

	def parse(self, response):
		# filename = response.url.split("/")[-2]
		# open(filename, 'wb').write(response.body)
		jdata=json.loads(response.body)
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
			channel['number'] = chan.xpath('div/strong/text()').extract()[0]
			channel['type'] = self.channelType
			items.append(channel)
		log.msg('{0} channels found'.format(len(items)),log.INFO)
		return items
