Scraper Vtr schedules
=============

Scrapy module that scrap the vtr page with schedule

## run spider standalone
Schedule spider allow scrap vtr epg available in http://televisionvtr.cl/programacion/, the spider scrap the site with many request or one request,
you can request from channel 1 to 10, 11 to 20, ..., 140 to 147 (gap=10) or all channel from 1 to 147 in one requests (gap=147).

schedule spider parameters:
* gap: gap between request (default = 10),
* top: max channel number (default = 147, max = 147)
* comuna: schedule city where scrap schedule (default = 'Santiago')
* channelType: channel type (default='series-peliculas')

run spider:
    scrapy crawl schedule -a top=3


## Fill program with external url pages

To fill programs with wikipedia url pages:
    python fill_wikipedia

To fill program with imdb path:
    python fill_imdb
