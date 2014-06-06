# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Channel(Item):
	# define the fields for your item here like:
	cod = Field()
	name = Field()
	description = Field()
	logo = Field()
	number = Field()
	type = Field()

class Program(Item):
	cod = Field()
	name = Field()
	description = Field()
	schedules = Field()
	photo = Field()
	genre = Field()
	actors = Field()
	director = Field()
	certification = Field()
	web = Field()
	episode = Field()

class Schedule(Item):
	chn = Field()
	prog = Field()
	duration = Field()
	start = Field()
	minificha = Field()
	ficha = Field()

