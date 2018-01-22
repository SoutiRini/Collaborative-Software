import json
import requests as req
from urllib.parse import urlunparse
from random import randint
from time import sleep

with open('bugzilla_bugs.json', 'r') as f:
    bugs = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}
comments = {}

for bug in bugs:
    urlbits = ['https', 'issues.apache.org', '/bugzilla/rest.cgi/bug/' + bug + '/comment', '', '', '']
    url = urlunparse(urlbits)
    print(url)
    resp = req(url, headers=headers)
    comments[bug] = resp.json['bugs'][bug]['comments']
    sleep(randint(1,20))

with open('bugzilla_comments.json', 'w') as f:
    json.dump(comments, f)
