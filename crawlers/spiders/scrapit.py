import scrapy
import datetime
from errorHandling import errback_httpbin
from makefolder import todayFolder
import json
from countersReport import addCounter
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ScrapSpider(scrapy.Spider):
    name = "scrapit"
    # request

    def start_requests(self):
        todayFolder(self)
        urls = [
            'http://www.dailyo.in/politics',
            'http://www.deccanchronicle.com/opinion',
        ]
        for url in urls:
            request = scrapy.Request(
                url=url, callback=self.parse, errback=errback_httpbin)
            yield request
            # self.log(getCounter('daily'))

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
                          "link": domain + news.css("a::attr(href)").extract_first(),
                          "source": domain,
                          }
                # yield deploy
                deccanchroniclearray.append(dcobj.copy())
                addCounter(domain)
            for news in res2:
                dcobj = {"title": news.css("a > h3::text").extract_first(),
                          "link": domain + news.css("a::attr(href)").extract_first(),
                          "source": domain,
                          }
                # yield deploy
                deccanchroniclearray.append(dcobj.copy())
                addCounter(domain)
            with open('./jsons/%s/%s.json' %(today,domain), 'w') as fp:
                    json.dump(deccanchroniclearray, fp)


        # www.dailyo.in parsing
        elif (domain == 'www.dailyo.in'):
            dailyoarray = []
            case2 = response.css('div#story_container > div > div.story-list')
            for news in case2:
                dailyoobj =  {"title": news.css("div.storybox > div.storytext > h2 > a::text").extract_first(),
                       "link": domain + news.css("div.storybox > div.storytext > h2 > a::attr(href)").extract_first(),
                       "source": domain,
                       }
                # yield deploy
                dailyoarray.append(dailyoobj.copy())
                addCounter(domain)
            with open('./jsons/%s/%s.json' %(today,domain), 'w') as fp:
                    json.dump(dailyoarray, fp)
        # with open('./counters/%s_daily-counters.json' %today, 'w') as fp:
        #         self.log(getCounter('daily'))
        #         json.dump(getCounter('daily'), fp)



