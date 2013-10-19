Scraper Vtr schedules
=============

Scrapy module that scraps the vtr page in http://televisionvtr.cl/programacion/ extracting Channels, Schedules and Programs tv and store this in a mongodb instance.

### Python dependencies

* Scrapy http://scrapy.org/
* pymongo
* Imdbpy http://imdbpy.sourceforge.net
* zope.interface
Can use pip http://www.pip-installer.org/en/latest/installing.html to install both.

(can you get in Mac OSX Mountain Lions: *error: Setup script exited with error: command 'clang' failed with exit status 1.* please try installing Command Line Tools of Xcode)

### Mongodb prerequisite

The scrapy by dedafult store the scraped data in mongodb instance, if you need change this process you can modifiy the default pipeline [http://doc.scrapy.org/en/0.18/topics/item-pipeline.html].

The database is **vtr** and the collections created are: **channels**, **schedules** and **programs**

## Channel spider

Channele spider scraps all channels available in the vtr webpage,


channel spider parameters:
* comuna: schedule city where scrap schedule (default = 'Santiago')
* channelType: channel type (default='series-peliculas')

### Channel schema

fields 		| type
----------- | ------------------------  
cod 		| int
name 		| string
description | string
logo		| string (url)
number      | int


### Run spider standalone

    scrapy crawl channels -a channelType='Infantil'

## Schedule spider
Schedule the spider scraps the site to get schedule and programs tv with many request or one request, you can request from channel 1 to 10, 11 to 20, ..., 140 to 147 (gap=10) or all channel from 1 to 147 in one requests (gap=147).

schedule spider parameters:
* gap: gap between request (default = 10),
* top: max channel number (default = 147, max = 147)
* comuna: schedule city where scrap schedule (default = 'Santiago')
* channelType: channel type (default='series-peliculas')


### Run spider standalone

    scrapy crawl schedule -a top=3


### Schedule Schema

fields 		| type
----------- | ------------------------  
chn 		| {cod: int, name: string}
duration 	| int (mins)
minificha 	| string (url)
canal_tipo  | string
prog        | {cod: int, name: string}
start		| datetime (YYYY MM DD HH:mm)

### Program schema

|	fields 		| type    			| optional	|
|---------------|-------------------|-----------|
|_id 		 	| int				|			|
|name 		 	| string			|			|
|description	| string			|			|
|episode		| string			|	true	|
|director 		| {name:string}		|	true	|
|actors			| [{name:string}]	|	true	|


## Run spiders in scrapy server

First start scrapy server, in the root vtrScrapy directory run:

        scrapy server

After in other terminal run* to scraps schedules and programs tv:

        curl http://localhost:6800/schedule.json -d project=default -d spider=schedule -d setting=DOWNLOAD_DELAY=2 -d top=3

* this run spider with DOWNLOAD_DELAY=2 and top argument equal 3


## Fill program with external url pages

To fill programs with wikipedia url pages:

    python fill_wikipedia

To fill program with imdb results:

	cd imdb/
    python imdbSearch.py -h

To fill imdb items:

	cd imdb/
    python imdbLoader.py -h

### IMDB item

fields 	| type		| optional
--------|-----------|-----
_id		|	int		|
genres	|	string	|	true
cast	|			|	true
writte	|			|	true
director|			|	true
year	| 	int		|
rating	|	float	|	true
votes	|			|	true
title	|	string	|
kind	| 	string	|



