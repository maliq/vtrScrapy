#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import Connection
from wikipedia import Wikipedia

conn= Connection()
db = conn.vtr
programs= db.programs
lang='es'
wiki = Wikipedia(lang)
print wiki.search('Wikipedia')

for program in programs.find():
    title = wiki.search(program['name'].encode('utf-8'))[0]['title']
    print title
    program['imdb_es']= title
    imdbField = 'imdb_'+lang
    programs.update({'_id':program['_id']}, {"$set": {imdbField:title}}, upsert=False)
