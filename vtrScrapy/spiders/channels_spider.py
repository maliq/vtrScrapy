import json
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from vtrScrapy.items import Schedule,Channel
from scrapy import log

class CanalesSpider(BaseSpider):
	name = "channels"

	def __init__(self, top=10,comuna='Santiago',channelType='series-peliculas'):
		# self.start_urls = ['http://televisionvtr.cl/index.php?obt=grilla&comuna=Santiago&canal_inicio=1&canal_cantidad=%s' % top]
		self.start_urls =['http://televisionvtr.cl/index.php?obt=grilla&canal_tipo=%s&comuna=%s' % (channelType,comuna)]

	def parse(self, response):
		# filename = response.url.split("/")[-2]
		# open(filename, 'wb').write(response.body)
		jdata=json.loads(response.body)
		# print jdata['canales']
		hxs = HtmlXPathSelector(text=jdata['canales'])
		channels = hxs.select('//li')
		items = []
		for chan in channels:
			channel = Channel()
			channel['cod'] = chan.select('@id').extract()[0]
			channel['name'] = chan.select('img/@alt').extract()[0]
			channel['logo'] = chan.select('img/@src').extract()[0]
			channel['description'] = chan.select('img/@title').extract()[0]
			channel['number'] = chan.select('div/strong/text()').extract()[0]
			items.append(channel)
		log.msg('{0} channels found'.format(len(items)),log.INFO)
		return items
