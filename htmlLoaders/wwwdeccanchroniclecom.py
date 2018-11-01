import sys
import collections
import scrapy
import json
params = {
    "title": "div > div > a > h3",
    "link": "div > div > a::attr(href)",
}

deploy = {}


def parsedeccanchronicle(logger, response):
    # page = 0
    for news in response.css('.opinionLanding > div'):
      
        yield {"title": news.css("div > a > h3::text").extract(),
               "link": news.css("div > a::attr(href)").extract(),
            #    "source": response.url,
               }
