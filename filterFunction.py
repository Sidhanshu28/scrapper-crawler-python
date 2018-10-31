from htmlLoaders.wwwdeccanchroniclecom import parsedeccanchronicle

def filter_out(logger,response):
        url = response.url
        logger.log(url)
        if url == 'https://www.deccanchronicle.com/opinion':
                parsedeccanchronicle(logger, response)
        else :
                logger.log("not found!")
                return