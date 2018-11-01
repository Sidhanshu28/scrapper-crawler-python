import os
import datetime

def todayFolder(logger):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    path = 'jsons/'+today
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        logger.log('directory exists!')