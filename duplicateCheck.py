import json
import requests
from requests.auth import HTTPBasicAuth


def duplicates(title):
    url = 'http://localhost:8888/scrap/wp-json/wp/v2/posts?slug='+title  # using for mac
#     url = 'http://localhost/wp-json/wp/v2/posts' #using for linux(office)
    r = requests.get(url)
    if len(r.text) >= 3:
        print(len(r.text))
        return 0
    else:
        return 1
