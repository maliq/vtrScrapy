#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import logging
import sys
sys.path.append("..")
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from vtrScrapy.spiders.imdb_result import ImdbSpider
from pymongo import Connection
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
from crawler_worker import CrawlerWorker

import argparse

"""
    Class to search in IMDB program and save the result in mongodb.
"""

class ImdbSearch(object):
    def __init__(self,mongodb='ml',maxResult=10, overwrite=False, maxPrograms=0):
        """
            Init method,
            mongodb : mongodb database, default ml
            maxResult : amount of result that search for each program, default 10
            overwrite : boolean parameter that overwrite if program have already imdb results, default False
            maxPrograms : how many program will process to imdb result search, dafault 0 that means all programs
        """
        conn= Connection()
        db = conn[mongodb]
        self.programs= db.programs
        self.maxResult= maxResult
        self.overwrite = overwrite
        self.maxPrograms = maxPrograms
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        logging.info('Mongodb initialized in %s db' % mongodb)

    def getResult(self,key):
        "This method return the result in imdb for given key"
        spider = ImdbSpider(key)
        result_queue = Queue()
        crawler = CrawlerWorker(spider, result_queue)
        crawler.start()
        results = result_queue.get()

        if len(results)>self.maxResult :
            del results[self.maxResult:]
        logging.debug('%s results', len(results))
        return results


    def process(self):
        """This method process program in mongodb backend"""
        for program in self.programs.find().limit(self.maxPrograms):
            # title = wiki.search(program['name'].encode('utf-8'))[0]['title']

            imdbResultField = 'imdb_results'
            imdbSelectedField = 'imdb_selected'
            if self.overwrite  or not(imdbResultField in program):
                results= isearch.getResult(program['name'])
                logging.debug('results: %s', results)
                if len(results)>0:
                    array=[]
                    for result in results:
                        array.append(dict(result))
                    imdb_selected=results[0]['imdbId']
                    program[imdbSelectedField]=results[0]['imdbId']
                    program[imdbResultField]= results
                    logging.debug('filling %s',program['name'])
                    self.programs.update({'_id':program['_id']}, {"$set": {imdbResultField:array,
                        imdbSelectedField:imdb_selected}}, upsert=False)
            else:
                logging.info('skiping %s',program['name'])

if __name__ == '__main__':
    # isearch = ImdbSearch(maxResult=5,overwrite=True)
    # isearch.process(maxProgramNumber=0)
    parser = argparse.ArgumentParser(description='Fill program with imdb results')
    parser.add_argument('-db','--database', help='Mongo database',required=True)
    parser.add_argument('-x','--maxResult',help='Max result to fill for program', default = 5)
    parser.add_argument('-p','--maxPrograms',help='How many programs will fill', default = 0)
    parser.add_argument('-ow','--overwrite',help='If overwrite old results if exists', default=False, action="store_true")
    args = parser.parse_args()


    isearch = ImdbSearch(mongodb=args.database, maxResult=args.maxResult,
        overwrite=args.overwrite, maxPrograms = args.maxPrograms)
    isearch.process()
    


