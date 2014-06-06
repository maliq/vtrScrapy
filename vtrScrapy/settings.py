# Scrapy settings for vtrScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'vtrScrapy'

SPIDER_MODULES = ['vtrScrapy.spiders']
NEWSPIDER_MODULE = 'vtrScrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'vtrScrapy_scraping (+http://www.toeska.cl)'

ITEM_PIPELINES = {
    'vtrScrapy.pipelines.StoreMongodbPipeline': 800
}


# LOG_LEVEL = 'INFO'
