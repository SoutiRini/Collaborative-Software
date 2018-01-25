import json
from torrequest import TorRequest
from urllib.parse import urlunparse
from random import randint
from time import sleep

with open('bugzilla_bugs.json', 'r') as f:
    bugs = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}
comments = {}

proxyPort = randint(10000, 45000)
controlPort = proxyPort + randint(1,10000)

bugs = [x for sublist in bugs for x in sublist]

with TorRequest(proxy_port=proxyPort, ctrl_port=controlPort, password=None) as tr:
    for bug in bugs:
        urlbits = ['https', 'issues.apache.org', '/bugzilla/rest.cgi/bug/' + str(bug) + '/comment', '', '', '']
        url = urlunparse(urlbits)
        print(url)
        try:
            resp = tr.get(url, headers=headers)
        except:
            print("Something went wrong. Trying again")
            sleep(randint(1,10))
            tr.reset_identity()
        j = resp.json()
        if (str(bug) in j['bugs']):
            comments[str(bug)] = resp.json()['bugs'][str(bug)]['comments']
        else:
            comments[str(bug)] = []
        sleep(randint(1,10))
        tr.reset_identity()

with open('bugzilla_comments.json', 'w') as f:
    json.dump(comments, f)
