import requests as req
import csv
from urllib.parse import urlunparse, urlencode
import json
from random import randint
from time import sleep

#https://issues.apache.org/bugzilla/rest.cgi/bug?limit=500&product=Ant

urlbits = ['https', 'issues.apache.org', '/bugzilla/rest.cgi/bug', '', '', '']
bugs = []
args = {
    'limit': 500,
    'offset': 0
}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}

while True:
    urlbits[4] = urlencode(args)
    url = urlunparse(urlbits)
    print(url)
    resp = req.get(url, headers=headers)
    newBugs = resp.json()['bugs']
    if not newBugs:
        break
    bugs.append([x['id'] for x in newBugs])
    args['offset'] = args['offset'] + args['limit']
    sleep(randint(1,20))

with open('bugzilla_bugs.json', 'w') as f:
    json.dump(bugs, f)
