import scrapy
import errorHandling

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ScrapSpider(scrapy.Spider):
    name = "scrapit"
    # request
    def start_requests(self):
        urls = [
           'http://www.dailyo.in/politics',
           'http://www.deccanchronicle.com/opinion',
           "http://www.httpbin.org/",
        ]
        i = 0
        for url in urls:
            i = i + 1   
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['counter'] = i
            yield request
            
    def parse(self, response):
        i = response.meta['counter']
        page = response.url.split("/")[-2]
        filename = 'news-%s-%d.html' %(page,i)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
