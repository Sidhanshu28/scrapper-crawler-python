import json
import requests
from requests.auth import HTTPBasicAuth


def sendData(testObj):
    url = 'http://localhost:8888/scrap/wp-json/wp/v2/posts'  #using for mac
#     url = 'http://localhost/wp-json/wp/v2/posts' #using for linux(office)
    r = requests.post(url, data=testObj, auth=HTTPBasicAuth(
        'sidhanshu', 'IJnJFAP$)4oqsRXoc1zZhmb&'))
