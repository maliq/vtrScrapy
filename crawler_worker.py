from scrapy import project, signals
from scrapy.crawler import Crawler
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
from scrapy.settings import Settings
from twisted.internet import reactor
import multiprocessing

class CrawlerWorker(multiprocessing.Process):

    def __init__(self, spider, result_queue):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue

        self.crawler = Crawler(Settings())
        self.crawler.configure()

        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)
        dispatcher.connect(self._stop_reactor, signal=signals.spider_closed)

    def _item_passed(self, item):
        self.items.append(item)

    def _stop_reactor(self):
        reactor.stop()

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        reactor.run()
        self.result_queue.put(self.items)
