import json
import os
from torrequest import TorRequest
from random import randint
from time import sleep

issueFolder = 'jira_issues'
comment_folder = 'jira_comments'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}

def getForProject(path):
    print('Processing ' + os.path.basename(path))
    proxyPort = randint(10000, 45000)
    controlPort = proxyPort + randint(1,10000)
    fullIssues = []
    with TorRequest(proxy_port=proxyPort, ctrl_port=controlPort, password=None) as tr:
        with open(path, 'r') as f:
            issues = json.load(f)
            issues = [x for sublist in issues for x in sublist] # flattening 
            for issue in issues:
                url = issue['self']
                print('Getting ' + url)
                try:
                    resp = tr.get(url, headers=headers)
                except:
                    print("Something went wrong. Trying again")
                    sleep(randint(1,10))
                    tr.reset_identity()
                j = resp.json()
                fullIssues.append(j)
                sleep(randint(1,10))
                tr.reset_identity()

    with open(os.path.join(comment_folder, os.path.basename(path))) as f:
        json.dump(fullIssues)

getForProject(os.path.join(issueFolder, 'aaaa.json'))

for entry in os.scandir(issueFolder):
    if entry.is_file():
        getForProject(entry.path)
