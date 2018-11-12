import json
import requests
from requests.auth import HTTPBasicAuth


def sendData(testObj):
    url = 'http://localhost:8888/scrap/wp-json/wp/v2/posts'
    r = requests.post(url, data=testObj, auth=HTTPBasicAuth(
        'scraper', '4Clp2OP)uO3bTtWC@Oc9UuH8'))
