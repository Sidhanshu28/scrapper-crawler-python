import json
import requests
from requests.auth import HTTPBasicAuth


def duplicates(title):
    new_title1 = '-'.join(title.split(" "))
    new_title = new_title1.lower()
    # proxies = { 'http': '192.168.0.159:80','https': '192.168.0.159:80'}
    # url = 'http://localhost:8888/scrap/wp-json/wp/v2/posts?slug='+new_title  # using for mac
    url = 'http://192.168.0.159/wp-json/wp/v2/posts?slug='+new_title #using for linux(office)
    r = requests.get(url, auth=HTTPBasicAuth(
        'sidhanshu', 'IJnJFAP$)4oqsRXoc1zZhmb&'))
        # 'P0l1t1clAdm1n', 'Politicl123@!@#$%^&*()'))
    if len(r.text) >= 3:
        print(len(r.text))
        return 0
    else:
        return 1
