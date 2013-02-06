#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from vtrScrapy.spiders.imdb_result import ImdbSpider
from pymongo import Connection
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
from crawler_worker import CrawlerWorker


conn= Connection()
db = conn.vtr
programs= db.programs



spider = ImdbSpider(key='la ley y el orden')
# crawler = Crawler(Settings())
# crawler.configure()
# crawler.crawl(spider)
# dispatcher.connect(self._item_passed, signals.item_passed)

# crawler.start()
# log.start()
# reactor.run() # the script will block here
result_queue = Queue()
crawler = CrawlerWorker(spider, result_queue)
crawler.start()
for item in result_queue.get():
    print item



