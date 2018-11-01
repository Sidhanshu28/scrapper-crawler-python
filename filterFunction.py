from htmlLoaders.wwwdeccanchroniclecom import parsedeccanchronicle
from scrapy import Selector

def filter_out(logger, response):
    url = response.url
    logger.log(url)
    if (url == 'https://www.deccanchronicle.com/opinion'):
        logger.log('here')
        # logger.log(response.css("div.opinionLanding > div > div > a > h3::text")[0].extract())
        parsedeccanchronicle(logger, response)
    else:
        logger.log("not found!")
       
