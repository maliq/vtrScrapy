#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import logging
from pymongo import Connection
from wikipedia import Wikipedia


class WikipediaSearch(object):
    def __init__(self,mlDb='ml',maxResult=10, overwrite=False,targetDir='./'):
        """
            Init method,
            mlDb : mongodb database
            maxResult : amount of result that search for each program, default 10
            overwrite : boolean parameter that overwrite if program have already wikipedia results, default False
            targetDir: directory where save the wikipedia articles downloaded
        """
        conn= Connection()
        db = conn[mlDb]
        self.programs = db.programs
        lang = 'en'
        self.wiki = Wikipedia(lang)
        self.maxResult = maxResult
        self.overwrite = overwrite
        self.targetDir = targetDir
        logging.info('Mongodb initialized in %s db for MovieLens' % mlDb)


    def fill(self,maxProgramNumber=10):
        """This method fill program in mongodb backend, maxProgramNumber parameter
        determine how many program will fill with wikipedia results
        """
        wikipediaResultsField = 'wikipediaResults'
        wikipediaSelectedField = 'wikipediaSelected'
        for program in self.programs.find().limit(maxProgramNumber):
            if self.overwrite  or not(wikipediaSelectedField in program):
                results = self.wiki.search2(program['name'].encode('utf-8'),self.maxResult)
                print results

                if len(results)>0:
                    selected=results[0]['title']
                    self.programs.update({'_id':program['_id']}, {"$set": {wikipediaResultsField:results, wikipediaSelectedField:selected}}, upsert=False)


    def downloadArticles(self,maxProgramNumber=10):
            """This method fill program in mongodb backend, maxProgramNumber parameter
            determine how many program will fill with wikipedia results
            """
            print 'running downloadArticles'
            wikipediaResultsField = 'wikipediaResults'
            wikipediaSelectedField = 'wikipediaSelected'
            for program in self.programs.find().limit(maxProgramNumber):
                # print program['name']
                # print program['wikipediaSelected']
                if wikipediaSelectedField in program:
                    filename = program[wikipediaSelectedField].encode('utf-8').replace (" ", "").replace ("/", "").replace (":", "")+".txt"
                    print 'writing: '+self.targetDir+filename
                    f = open(self.targetDir+filename,'w')
                    rawArticle = self.wiki.article(program[wikipediaSelectedField].encode('utf-8'))
                    f.write(rawArticle)
                    f.close()


if __name__ == '__main__':
    # wsearch = WikipediaSearch(maxResult=5,overwrite=True)
    # wsearch.fill(maxProgramNumber=0)
    wsearch = WikipediaSearch(maxResult=5,overwrite=True,targetDir='/Users/maliq/Documents/tmp/wikiRaw/')
    wsearch.downloadArticles(maxProgramNumber=100)
