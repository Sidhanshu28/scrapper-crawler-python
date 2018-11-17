import json
import requests
from requests.auth import HTTPBasicAuth


def duplicates(title):
    new_title1 = '-'.join(title.split(" "))
    new_title = new_title1.lower()
    url = 'http://localhost:8888/scrap/wp-json/wp/v2/posts?slug='+new_title  # using for mac
    # url = 'http://localhost/wp-json/wp/v2/posts?slug='+new_title #using for linux(office)
    r = requests.get(url)
    if len(r.text) >= 3:
        print(len(r.text))
        return 0
    else:
        return 1
