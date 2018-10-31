
def parsedeccanchronicle(logger, response):
    page = response.url.split("/")[-2]
    filename = 'news-%s.html' %(page)
    with open(filename, 'wb') as f:
        f.write(response.body)
    logger.log('Saved file %s' % filename)