import json
import os
from torrequest import TorRequest

issueFolder = 'jira_issues'
comment_folder = 'jira_comments'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}

for entry in os.walk(issueFolder):
    if entry.isFile():
        getForProject(entry.path)

def getForProject(path):
    proxyPort = randint(10000, 45000)
    controlPort = proxyPort + randint(1,10000)
    fullIssues = []
    with TorRequest(proxy_port=proxyPort, ctrl_port=controlPort, password=None) as tr:
        with open(path, 'r') as f:
            issues = json.load(f)
            for issue in issues[0]:
                url = issue['self']
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
