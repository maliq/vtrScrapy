#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import logging
import argparse
from imdb import IMDb
from pymongo import Connection
from scrapy.item import Item, Field

class ImdbProgram(Item):
    _id = Field()
    genres = Field()
    cast = Field()
    writter =Field()
    director =Field()
    year = Field()
    rating =Field()
    votes = Field()
    title = Field()
    kind = Field()

"""
    Class to fill the result selected from imdb result search
"""
class ImdbLoader(object):
    def __init__(self,db='ml', overwrite = False, maxPrograms = 0):
        conn= Connection()
        db = conn[db]
        self.programs= db.programs
        self.imdbs = db.imdbs
        self.overwrite = overwrite
        self.maxPrograms = maxPrograms
        self.ia = IMDb()
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logging.info('Mongodb initialized in %s db', db)

    def saveImdbItem(self, imdbId):
        m = self.ia.get_movie(imdbId)
        current_imdb_item = self.imdbs.find_one({"_id": imdbId})
        if self.overwrite or not current_imdb_item:
            ip=ImdbProgram()
            ip['_id']=imdbId
            ip['title'] = m['title']
            # ip['cast']= m['cast']
            ip['year'] = m['year']
            # m['director']
            # m['writer']
            ip['kind']=m['kind']
            if 'rating' in m:
                ip['rating']=m['rating']
            if 'votes' in m:
                ip['votes']=m['votes']
            if 'genres' in m:
                ip['genres']=m['genres']
            logging.info('saving imdb item %s \n', ip)
            if not current_imdb_item:
                self.imdbs.insert(dict(ip))
            else:
                self.imdbs.update({"_id": imdbId},dict(ip))
        else:
            logging.info('skip imdbId: %s, already exists', imdbId)

    def process(self):
        for program in self.programs.find().limit(self.maxPrograms):
            imdbSelectedField = 'imdb_selected'
            downloadedField = 'loaded'
            if(imdbSelectedField in program):
                imdbId = program[imdbSelectedField]
                self.saveImdbItem(imdbId)
            else:
                logging.warning('skip %s because doesnt have %s field', program['name'], imdbSelectedField)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill program with imdb data')
    parser.add_argument('-db','--database', help='Mongo database',required=True)
    parser.add_argument('-p','--maxPrograms',help='How many programs will fill', default = 0, type=int)
    parser.add_argument('-ow','--overwrite',help='If overwrite old results if exists', default=False, action="store_true")
    args = parser.parse_args()
    ipl = ImdbLoader(db=args.database,
        overwrite=args.overwrite, maxPrograms = args.maxPrograms)
    ipl.process()


