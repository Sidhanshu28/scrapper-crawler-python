import scrapy
import datetime
import re
from errorHandling.errorHandling import errback_httpbin
from makefolder.makefolder import todayFolder
import json
import requests
from requests.auth import HTTPBasicAuth
from countersReport.countersReport import addCounter
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from databaseConnector.databaseConnector import sendData
from duplicateCheck.duplicateCheck import duplicates
import time
# import schedule


class ScrapSpider(scrapy.Spider):
    name = "scrapit"
    # request
    


    def start_requests(self):
        # todayFolder(self)
        urls = [
            # "http://www.dailyo.in/politics",
            "http://www.deccanchronicle.com/opinion",
            # "http://www.firstpost.com/category/politics",
            # "http://www.forbesindia.com",
            # "http://www.frontline.in",
            # "http://www.hindustantimes.com/opinion/",
            # "http://www.ndtv.com/opinion",
            # "http://www.news18.com/blogs",
            # "https://www.outlookindia.com/website",
            # "https://www.outlookindia.com/magazine",
            # "http://scroll.in",
            # "https://blogs.economictimes.indiatimes.com",
            # "https://www.thehindu.com/opinion/", 
            # "https://www.thehindubusinessline.com/opinion/",
            # "http://qrius.com", 
            # "http://www.indianexpress.com/opinion", 
            # "http://www.newindianexpress.com/Opinions",
            # "http://www.dailypioneer.com/columnists",
            # "http://blogs.timesofindia.indiatimes.com",
            # "https://www.tribuneindia.com/news/opinion/",
            # "https://thewire.in",
            # "https://www.telegraphindia.com/opinion",
            # "http://www.rediff.com/news/interviews10.html",
            # "http://www.rediff.com/news/columns10.html",
            # "https://www.huffingtonpost.in/blogs",
            # "https://www.dnaindia.com/analysis",
            # "http://www.livemint.com/opinion/",
            # "http://www.financialexpress.com/print/edits-columns"
        ]
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in urls:
            request = scrapy.Request(
                url=url, callback=self.parse,errback= errback_httpbin, headers=headers)
            yield request

    def parse(self, response):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        domain = (response.url).split('/')[2]
        urlhead = (response.url).split('://')[0]+"://"
        self.log(response.url)
        # www.deccanchronicle.com parsing
        if (domain == 'www.deccanchronicle.com'):
            deccanchroniclearray = []
            case = response.css('div.opinionLanding > div')[0]
            res = case.css('div.opnionTopSmall')
            res2 = case.css('div.opnionTopBig')
            for news in res:
                dcobj = {"title": news.css("a > h3::text").extract_first(),
                         "source_link": urlhead + domain + news.css("a::attr(href)").extract_first(),
                         "slug": news.css("a > h3::text").extract_first(),
                         "status": "publish"
                         }
                title = (news.css("a > h3::text").extract_first()
                         ).replace(",", "")
                title = title.replace("&","")
                duplicate = duplicates(title)

                if duplicate == 1:
                    # data sender function
                    sendData(dcobj)
                    #addCounter(domain)
                # yield deploy
                deccanchroniclearray.append(dcobj.copy())
            for news in res2:
                dcobj = {"title": news.css("a > h3::text").extract_first(),
                         "source_link": urlhead + domain + news.css("a::attr(href)").extract_first(),
                         "slug": news.css("a > h3::text").extract_first(),
                         "status": "publish"
                         }

                title = (news.css("a > h3::text").extract_first()
                         ).replace(",", "")
                title = title.replace("&","")
                duplicate = duplicates(title)
                if duplicate == 1:
                    # data sender function
                    sendData(dcobj)
                    #addCounter(domain)
                # yield deploy
                deccanchroniclearray.append(dcobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(deccanchroniclearray, fp)

        # www.dailyo.in parsing
        elif (domain == 'www.dailyo.in'):
            dailyoarray = []
            case2 = response.css('div#story_container > div > div.story-list')
            for index, news in zip(range(5), case2):
                dailyoobj = {"title": news.css("div.storybox > div.storytext > h2 > a::text").extract_first(),                                  "source_link": urlhead + domain + news.css("div.storybox > div.storytext > h2 > a::attr(href)") .extract_first(),
                             "slug": news.css("div.storybox > div.storytext > h2 > a::text").extract_first(),
                             "status": "publish"
                             }
                title = (news.css(
                    "div.storybox > div.storytext > h2 > a::text").extract_first()).replace(",", "")
                title = title.replace("&","")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(dailyoobj)
                    #addCounter(domain)
                # yield deploy
                dailyoarray.append(dailyoobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(dailyoarray, fp)

        # www.forbesindia.com parsing
        elif (domain == 'www.forbesindia.com'):
            forbesarray = []
            case2 = response.css(".carousel > .carousel-inner > .item")
            for index, news in zip(range(5), case2):
                forbesobj = {"title": news.css(".carousel-caption > h3 > a::text").extract_first(),                                             "source_link": urlhead + domain + news.css(".carousel-caption > h3 > a::attr(href)").extract_first(),
                             "slug": news.css(".carousel-caption > h3 > a::text").extract_first(),
                             "status": "publish"
                             }
                title = (
                    news.css(".carousel-caption > h3 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(forbesobj)
                    #addCounter(domain)
                # yield deploy
                forbesarray.append(forbesobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(forbesarray, fp)

        # www.frontline.in parsing
        elif (domain == 'www.frontline.in'):
            frontlinearray = []
            case2 = response.css(".latestInner")
            for index, news in zip(range(5), case2):
                frontlineobj = {"title": news.css("h2 > a::text").extract_first(),                                                                 "source_link": news.css("h2 > a::attr(href)").extract_first(),
                                "slug": news.css("h2 > a::text").extract_first(),
                                "status": "publish"
                                }
                title = (
                    news.css("h2 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                self.log(duplicate)
                if duplicate == 1:
                     # data sender function
                    sendData(frontlineobj)
                    #addCounter(domain)
                # yield deploy
                frontlinearray.append(frontlineobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(frontlinearray, fp)

        # www.hindustantimes.com/opinion parsing
        elif (domain == 'www.hindustantimes.com'):
            htarray = []
            case2 = response.css(".media-heading")
            for index, news in zip(range(3), case2):
                htobj = {"title": news.css("a::text").extract_first(),                                                                 "source_link": news.css("a::attr(href)").extract_first(),
                         "slug": news.css("a::text").extract_first(),
                         "status": "publish"
                         }
                
                title = (news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(htobj)
                    #addCounter(domain)
                # yield deploy
                htarray.append(htobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(htarray, fp)

        # www.ndtv.com/opinion parsing
        elif (domain == 'www.ndtv.com'):
            ndtvarray = []
            case2 = response.css(".nopinion")
            for index, news in zip(range(5), case2):
                ndtvobj = {"title": news.css(".opinion_blog_contentwrap > .opinion_blog_header > a::text").extract_first(),            "source_link": news.css(".opinion_blog_contentwrap > .opinion_blog_header > a::attr(href)").extract_first(),
                           "slug": news.css(".opinion_blog_contentwrap > .opinion_blog_header > a::text").extract_first(),
                           "status": "publish"
                           }
                title = (
                    news.css(".opinion_blog_contentwrap > .opinion_blog_header > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(ndtvobj)
                    #addCounter(domain)
                # yield deploy
                ndtvarray.append(ndtvobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(ndtvarray, fp)

        # www.news18.com/blogs parsing
        elif (domain == 'www.news18.com'):
            n18array = []
            case2 = response.css(".author-list")
            for index, news in zip(range(5), case2):
                n18obj = {"title": news.css("div.item-wrap > .item-front > .item-cont > h3 > a::text").extract_first(),            "source_link": news.css("div.item-wrap > .item-front > .item-cont > h3 > a::attr(href)").extract_first(),
                          "slug": news.css("div.item-wrap > .item-front > .item-cont > h3 > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("div.item-wrap > .item-front > .item-cont > h3 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(n18obj)
                    #addCounter(domain)
                # yield deploy
                n18array.append(n18obj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(n18array, fp)

        # www.outlookindia.com/website parsing
        elif (domain == 'www.outlookindia.com'):
            oliarray = []
            case2 = response.css(".listing > ul > li")
            for index, news in zip(range(2), case2):
                oliobj = {"title": news.css(".content_serach > .cont_head > a::text").extract_first(),            
                "source_link": "http://"+ domain + news.css(".content_serach > .cont_head > a::attr(href)").extract_first(),
                          "slug": news.css(".content_serach > .cont_head > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css(".content_serach > .cont_head > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(oliobj)
                    #addCounter(domain)
                # yield deploy
                oliarray.append(oliobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(oliarray, fp) 

        # scroll.in parsing
        elif (domain == 'scroll.in'):
            newarray = []
            # case2 = response.css(".listing > ul > li")
            # for index, news in zip(range(5), case2):
            newobj = {"title": response.css(".featured-story > a >.row-story > h1::text").extract_first(),
                      "source_link": response.css(".featured-story > a::attr(href)").extract_first(),
                      "slug": response.css(".featured-story > a >.row-story > h1::text").extract_first(),
                      "status": "publish"
                      }
            title = (
                response.css(".featured-story > a >.row-story > h1::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                    # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())

            case2 = response.css(
                ".listing > ul > li.basic-collection-stories > ul > li")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("a > div.raw-story-meta > h1::text").extract_first(),
                          "source_link": news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a > div.raw-story-meta > h1::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a > div.raw-story-meta > h1::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                        # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # blogs.economictimes.indiatimes.com parsing
        elif (domain == 'economictimes.indiatimes.com'):
            newarray = []
            case2 = response.css(".article")
            for index, news in zip(range(5), case2):
                newobj = {"title": news.css(".media-body > .media-heading > a::text").extract_first(),                              "source_link": news.css(".media-body > .media-heading > a::attr(href)").extract_first(),
                          "slug": news.css(".media-body > .media-heading > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css(".media-body > .media-heading > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.financialexpress.com/print/edits-columns parsing
        elif (domain == 'www.financialexpress.com'):
            newarray = []
            # case2 = response.css(".article")
            # for index, news in zip(range(5), case2):
            newobj = {"title": response.css(".listtopbox > .pstsummary > .lsttitle > a::text").extract_first(),                              "source_link": response.css(".listtopbox > .pstsummary > .lsttitle > a::attr(href)").extract_first(),
                        "slug": response.css(".listtopbox > .pstsummary > .lsttitle > a::text").extract_first(),
                        "status": "publish"
                        }
            title = (
                response.css(".listtopbox > .pstsummary > .lsttitle > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                    # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

            case2 = response.css(".lstitemt")
            for index, news in zip(range(5), case2):
                newobj = {"title": news.css(".listcontent > .lstitems > a::text").extract_first(),                              "source_link": news.css(".listcontent > .lstitems > a::attr(href)").extract_first(),
                        "slug": news.css(".listcontent > .lstitems > a::text").extract_first(),
                        "status": "publish"
                        }
                title = (
                    news.css(".listcontent > .lstitems > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                    # data sender function
                    sendData(newobj)
                    #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.thehindu.com/opinion parsing
        elif (domain == 'www.thehindu.com'):
            newarray = []
            case2 = response.css(".ES2-100x4-text1")
            for index, news in zip(range(5), case2):
                newobj = {"title": news.css("h2 > a::text").extract_first(),
                        "source_link": news.css("h2 > a::attr(href)").extract_first(),
                          "slug": news.css("h2 > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("h2 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.thehindubusinessline.com/opinion parsing
        elif (domain == 'www.thehindubusinessline.com'):
            newarray = []
            case2 = response.css("h2.op-title")
            for index, news in zip(range(5), case2):
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.thehindubusinessline.com/opinion parsing
        elif (domain == 'www.thehindubusinessline.com'):
            newarray = []
            case2 = response.css("h2.op-title")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            newobj = {"title": response.css("h2.ed-ts > a::text").extract_first(),
                        "source_link": response.css("h2.ed-ts > a::attr(href)").extract_first(),
                          "slug": response.css("h2.ed-ts > a::text").extract_first(),
                          "status": "publish"
                          }
            title = (response.css("h2.ed-ts > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.dnaindia.com/analysis parsing
        elif (domain == 'www.dnaindia.com'):
            newarray = []
            case2 = response.css(".opinionsubldbx")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("h3 > a::text").extract_first(),
                        "source_link": "https://" + domain + news.css("h3 > a::attr(href)").extract_first(),
                          "slug": news.css("h3 > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("h3 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            newobj = {"title": response.css(".opiniontpbx > h3 > a::text").extract_first(),
                        "source_link": "https://" + domain + response.css(".opiniontpbx > h3 > a::attr(href)").extract_first(),
                          "slug": response.css(".opiniontpbx > h3 > a::text").extract_first(),
                          "status": "publish"
                          }
            title = (response.css(".opiniontpbx > h3 > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.firstpost.com/category/politics parsing
        elif (domain == 'www.firstpost.com'):
            newarray = []
            case2 = response.css(".panel-body > ul.single-column > li")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("a > p::text").extract_first(),
                        "source_link": news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a > p::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a > p::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            newobj = {"title": response.css(".news-item > a > h1::text").extract_first(),
                        "source_link": response.css(".news-item > a::attr(href)").extract_first(),
                          "slug": response.css(".news-item > a > h1::text").extract_first(),
                          "status": "publish"
                          }
            title = (response.css(".news-item > a > h1::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.telegraphindia.com/opinion parsing
        elif (domain == 'www.telegraphindia.com'):
            newarray = []
            case2 = response.css(".storyDetailsRight")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("h3 > a::text").extract_first(),
                        "source_link": "https://"+ domain + news.css("h3 > a::attr(href)").extract_first(),
                          "slug": news.css("h3 > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("h3 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            newobj = {"title": response.css(".storyDetailsLeft > h3 > a::text").extract_first(),
                        "source_link": "https://"+ domain + response.css(".storyDetailsLeft > h3 > a::attr(href)").extract_first(),
                          "slug": response.css(".storyDetailsLeft > h3 > a::text").extract_first(),
                          "status": "publish"
                          }
            title = (response.css(".storyDetailsLeft > h3 > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # thewire.in/category/politics/all parsing
        elif (domain == 'thewire.in'):
            newarray = []
            case2 = response.css(".card__title")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": "https://"+ domain + news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.tribuneindia.com/news/opinion/ parsing
        elif (domain == 'www.tribuneindia.com'):
            newarray = []
            case2 = response.css(".OpLeft > h2")
            for index, news in zip(range(5), case2):
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": "https://" + domain + news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # blogs.timesofindia.indiatimes.com parsing
        elif (domain == 'timesofindia.indiatimes.com'):
            newarray = []
            case2 = response.css(".article")
            for index, news in zip(range(5), case2):
                newobj = {"title": news.css(".media-body > .media-heading > a::text").extract_first(),
                        "source_link": news.css(".media-body > .media-heading > a::attr(href)").extract_first(),
                          "slug": news.css(".media-body > .media-heading > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css(".media-body > .media-heading > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.dailypioneer.com/columnists parsing
        elif (domain == 'www.dailypioneer.com'):
            newarray = []
            # case2 = response.css(".article")
            # for index, news in zip(range(5), case2):
            newobj = {"title": response.css(".BigNews > h2 > a::text").extract_first(),
                      "source_link": "https://" + domain + "/columnists" + response.css(".BigNews > h2 > a::attr(href)").extract_first(),
                        "slug": response.css(".BigNews > h2 > a::text").extract_first(),
                        "status": "publish"
                        }
            title = (
                   response.css(".BigNews > h2 > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # www.newindianexpress.com/Opinions parsing
        elif (domain == 'www.newindianexpress.com'):
            newarray = []
            case2 = response.css(".sub_opinion_main")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("h5 > a::text").extract_first(),
                        "source_link": news.css("h5 > a::attr(href)").extract_first(),
                          "slug": news.css("h5 > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("h5 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # qrius.com parsing
        elif (domain == 'qrius.com'):
            newarray = []
            case2 = response.css(".imgpost")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css(".textbox > p > a::text").extract_first(),
                        "source_link": news.css(".textbox > p > a::attr(href)").extract_first(),
                          "slug": news.css(".textbox > p > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css(".textbox > p > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # indianexpress.com/opinion parsing
        elif (domain == 'indianexpress.com'):
            newarray = []
            case2 = response.css(".opi-story")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("h6 > a::text").extract_first(),
                        "source_link": news.css("h6 > a::attr(href)").extract_first(),
                          "slug": news.css("h6 > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("h6 > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            newobj = {"title": response.css(".leadstory > h6 > a::text").extract_first(),
                        "source_link": response.css(".leadstory > h6 > a::attr(href)").extract_first(),
                          "slug": response.css(".leadstory > h6 > a::text").extract_first(),
                          "status": "publish"
                          }
            title = (response.css(".leadstory > h6 > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # http://www.rediff.com/news/interviews10.html parsing
        elif (domain == 'www.rediff.com'):
            newarray = []
            case2 = response.css(".column")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css(".outborder > .ingap > p > a::text").extract_first(),
                        "source_link": news.css(".outborder > .ingap > p > a::attr(href)").extract_first(),
                          "slug": news.css(".outborder > .ingap > p > a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css(".outborder > .ingap > p > a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # https://www.huffingtonpost.in/blogs/ parsing draft posts
        elif (domain == 'www.huffingtonpost.in'):
            newarray = []
            # self.log(response)
            case2 = response.css("ul.card__headlines > li.card__entry > h3.card__headline")
            for index,news in zip(range(30),case2):
                self.log(news.css("a::text").extract_first())
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "draft"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

        # http://www.livemint.com/opinion parsing
        elif (domain == 'www.livemint.com'):
            newarray = []
            case2 = response.css(".lead-stories-section-left > article")
            for index, news in zip(range(3), case2):
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": "http://" + domain + news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            case3 = response.css(".lead-stories-section-right > div > .lead-stories-section-right-2 > article")
            for index, news in zip(range(3), case3):
                newobj = {"title": news.css("a::text").extract_first(),
                        "source_link": "http://" + domain + news.css("a::attr(href)").extract_first(),
                          "slug": news.css("a::text").extract_first(),
                          "status": "publish"
                          }
                title = (
                    news.css("a::text").extract_first()).replace(",", "")
                duplicate = duplicates(title)
                if duplicate == 1:
                     # data sender function
                    sendData(newobj)
                    #addCounter(domain)
                # yield deploy
                newarray.append(newobj.copy())

            newobj = {"title": response.css(".lead-stories-section-right > div > .lead-stories-section-right-1 > h1 > a::text").extract_first(),
                        "source_link": "http://" + domain + response.css(".lead-stories-section-right > div > .lead-stories-section-right-1 > h1 > a::attr(href)").extract_first(),
                        "slug": response.css(".lead-stories-section-right > div > .lead-stories-section-right-1 > h1 > a::text").extract_first(),
                          "status": "publish"
                          }
            title = (response.css(".lead-stories-section-right > div > .lead-stories-section-right-1 > h1 > a::text").extract_first()).replace(",", "")
            duplicate = duplicates(title)
            if duplicate == 1:
                # data sender function
                sendData(newobj)
                #addCounter(domain)
            # yield deploy
            newarray.append(newobj.copy())
            #with open('./jsons/%s/%s.json' % (today, domain), 'w') as fp:
                #json.dump(newarray, fp)

# inst = ScrapSpider() 

# schedule.every(1).minutes.do(inst.start_requests)

# while True:
#     schedule.run_pending()
#     time.sleep(1)