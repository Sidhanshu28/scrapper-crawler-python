import scrapy
import datetime
import re
from errorHandling import errback_httpbin
from makefolder import todayFolder
import json
import requests
from requests.auth import HTTPBasicAuth
from countersReport import addCounter
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from databaseConnector import sendData
from duplicateCheck import duplicates


class ScrapSpider(scrapy.Spider):
    name = "scrapit"
    # request

    def start_requests(self):
        todayFolder(self)
        urls = [
            "http://www.dailyo.in/politics",
            "http://www.deccanchronicle.com/opinion",
            # "http://www.dnaindia.com/analysis",
            # "http://www.firstpost.com/category/politics",
            # "http://www.forbesindia.com",
            # "http://www.frontline.in",
            # "http://www.hindustantimes.com/opinion",
            # "http://indiatoday.intoday.in/calendar",
            # "http://www.livemint.com/opinion",
            # "http://www.ndtv.com/opinion",
            # "http://www.news18.com/blogs",
            # "http://www.outlookindia.com/website",
            # "http://www.outlookindia.com/magazine",
            # "http://www.rediff.com/news/interviews10.html",
            # "http://www.rediff.com/news/columns10.html",
            # "http://scroll.in",
            # "https://blogs.economictimes.indiatimes.com",
            # "http://www.financialexpress.com/print/edits-columns",
            # "http://www.thehindu.com/opinion",
            # "http://www.thehindubusinessline.com/opinion",
            # "http://www.huffingtonpost.in/the-blog",
            # "http://theindianeconomist.com",
            # "http://indianexpress.com/opinion",
            # "http://www.newindianexpress.com/Opinions",
            # "http://www.dailypioneer.com/columnists",
            # "http://blogs.timesofindia.indiatimes.com",
            # "http://www.tribuneindia.com/news/opinion",
            # "http://hewire.in",
            # "https://www.telegraphindia.com/opinion",
        ]
        for url in urls:
            request = scrapy.Request(
                url=url, callback=self.parse, errback=errback_httpbin)
            yield request

    def parse(self, response):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        domain = (response.url).split('/')[2]

        # www.deccanchronicle.com parsing
        if (domain == 'www.deccanchronicle.com'):
            deccanchroniclearray = []
            case = response.css('div.opinionLanding > div')[0]
            res = case.css('div.opnionTopSmall')
            res2 = case.css('div.opnionTopBig')
            for news in res:
                dcobj = {"title": news.css("a > h3::text").extract_first(),
                        #  "meta": [{
                             "link": domain + news.css("a::attr(href)").extract_first(),
                            #  }],
                         "content": domain,
                         "slug": news.css("a > h3::text").extract_first(),
                         "status": "publish"
                         }
                title = (news.css("a > h3::text").extract_first()
                         ).replace(",", "")
                new_title = '-'.join(title.split(" "))
                self.log(new_title.lower())
                duplicate = duplicates(new_title.lower())
                if duplicate == 1:
                    # data sender function
                    sendData(dcobj)
                    # yield deploy
                    deccanchroniclearray.append(dcobj.copy())
                    addCounter(domain)
            for news in res2:
                dcobj = {"title": news.css("a > h3::text").extract_first(),
                        #  "meta":[{
                             "link": domain + news.css("a::attr(href)").extract_first(),
                            #  }],
                         "content": domain,
                         "slug": news.css("a > h3::text").extract_first(),
                         "status": "publish"
                         }

                title = (news.css("a > h3::text").extract_first()
                         ).replace(",", "")
                new_title = '-'.join(title.split(" "))
                self.log(new_title.lower())
                duplicate = duplicates(new_title.lower())
                if duplicate == 1:
                    # data sender function
                    sendData(dcobj)
                    # yield deploy
                    deccanchroniclearray.append(dcobj.copy())
                    addCounter(domain)
            with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                json.dump(deccanchroniclearray, fp)

        # www.dailyo.in parsing
        elif (domain == 'www.dailyo.in'):
            dailyoarray = []
            case2 = response.css('div#story_container > div > div.story-list')
            for news in case2:
                dailyoobj = {"title": news.css("div.storybox > div.storytext > h2 > a::text").extract_first(),
                            #  "meta":[{
                                 "link": domain + news.css("div.storybox > div.storytext > h2 > a::attr(href)").extract_first(),
                                #  }],
                             "content": domain,
                             "slug": news.css("div.storybox > div.storytext > h2 > a::text").extract_first(),
                             "status": "publish"
                             }

                title = (news.css(
                    "div.storybox > div.storytext > h2 > a::text").extract_first()).replace(",", "")
                new_title = '-'.join(title.split(" "))
                duplicate = duplicates(new_title.lower())
                if duplicate == 1:
                     # data sender function
                    sendData(dailyoobj)
                    # yield deploy
                    dailyoarray.append(dailyoobj.copy())
                    addCounter(domain)
            with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                json.dump(dailyoarray, fp)
