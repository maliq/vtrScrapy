Scraper Vtr schedules
=============

Scrapy module that scrap the vtr page with schedule

## Schedule spider
Schedule spider allow scrap vtr epg available in http://televisionvtr.cl/programacion/, the spider scrap the site with many request or one request,
you can request from channel 1 to 10, 11 to 20, ..., 140 to 147 (gap=10) or all channel from 1 to 147 in one requests (gap=147).

schedule spider parameters:
* gap: gap between request (default = 10),
* top: max channel number (default = 147, max = 147)
* comuna: schedule city where scrap schedule (default = 'Santiago')
* channelType: channel type (default='series-peliculas')


### Run spider standalone

    scrapy crawl schedule -a top=3


### Run spider in scrapy server

First start scrapy server, in the root vtrScrapy directory run:

        scrapy server

After in other terminal run*:

        curl http://localhost:6800/schedule.json -d project=default -d spider=schedule -d setting=DOWNLOAD_DELAY=2 -d top=3

* this run spider with DOWNLOAD_DELAY=2 and top argument equal 3

## Fields for Program and Schedule

### Program

|	fields 		| type    			| optional	|
|---------------|-------------------|-----------|
|_id 		 	| int				|			|
|name 		 	| string			|			|
|description	| string			|			|
|episode		| string			|	true	|
|director 		| {name:string}		|	true	|
|actors			| [{name:string}]	|	true	|


### Schedule

fields 		| type
----------- | ------------------------  
chn 		| {cod: int, name: string}
duration 	| int (mins)
minificha 	| string (url)
canal_tipo  | string
prog        | {cod: int, name: string}
start		| datetime (YYYY MM DD HH:mm)



## Fill program with external url pages

To fill programs with wikipedia url pages:

    python fill_wikipedia

To fill program with imdb path:

    python fill_imdb
