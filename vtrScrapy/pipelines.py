# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import json
import pymongo
from scrapy import log
from pymongo import Connection
from vtrScrapy.items import Schedule,Channel,Program

class StoreMongodbPipeline(object):
    def __init__(self):
        conn= Connection()
        db = conn.vtr
        self.channels = db.channels
        self.schedules = db.schedules
        self.programs= db.programs
        log.msg('Mongodb initialized in pipeline',log.INFO)

    def process_item(self, item, spider):
        log.msg('processing item {0}'.format(item),log.DEBUG)
        if type(item) == Channel:
            log.msg('Saving item like channel',log.DEBUG)
            self.channels.insert(dict(item))
        elif isinstance(item,Schedule):
            log.msg('Saving item like schedule',log.DEBUG)
            self.schedules.insert(dict(item))
        elif isinstance(item,Program):
            log.msg('Saving item like program',log.DEBUG)
            self.programs.insert(dict(item))
        else:
            log.msg('{0} doesn\'t match with channel,schedule or program'.format(item),log.WARNING)
        return item
