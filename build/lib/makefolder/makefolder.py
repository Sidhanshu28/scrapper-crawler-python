import os
import datetime
import pkgutil

def todayFolder(logger):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    path = 'jsons/'+today
    data = pkgutil.get_data("project", path)

    if not data:
        os.mkdir(path)
    else:
        logger.log('directory exists!')