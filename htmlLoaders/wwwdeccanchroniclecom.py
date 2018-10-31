

params = {
    "title":"div > div > a > h3",
    "link" : "div > div > a::attr(href)",
}

def parsedeccanchronicle(logger, response):
    # page = response.url.split("/")[-2]
    # filename = 'news-%s.html' %(page)
    # with open(filename, 'wb') as f:
    #     f.write(response.body)
    # logger.log('Saved file %s' % filename)

    for news in response.css('div.opinionLanding'):
        yield {
            "title": news.css(params['title']+"::text").extract(),
            "link": news.css(params['link']+"::text").extract(),
            "source": response.url
        }