import csv
from urllib.parse import urlparse, urlencode, urlunparse
from torrequest import TorRequest
from random import randint
from time import sleep

def parseUrl(url):
    o = urlparse(url)
    if 'secure' in o.path:
        id = o.query.split("=")[1]
        return id
    else:
        return o.path.strip('/').split('/')[-1]

urlbits = ['https', 'issues.apache.org', '/jira/rest/api/2/search', '', '', '']
#urlRoot = 'https://issues.apache.org/jira/rest/api/2/search?jql=project=%2210471%22&maxResults:%222000%22'
args = {
    'maxResults': 500
}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}

def getProjectIssues(project_id, startAt = 0):
    args['project'] = project_id
    args['startAt'] = startAt
    issues = []
    with TorRequest() as tr:
        while True:
            urlbits[4] = urlencode(args)
            print(urlunparse(urlbits))
            try:
                resp = tr.get(urlunparse(urlbits), headers = headers)
            except:
                print('Something went wrong. Trying again.')
                tr.reset_identity()
                sleep(randint(1, 10)):
                    pass))
                continue
            j = resp.json()
            issues.append(j['issues'])
            args['startAt'] = j['maxResults'] + j['startAt']
            if j['total'] <= j['maxResults'] + j['startAt']:
                break
            sleep(randint(1,10))
            tr.reset_identity()
    return issues

with open('jira-projects.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        project = row[0]
        project_id = parseUrl(row[1])
        issues = getProjectIssues(project_id)
        json.dump(issues, "jira_issues/" +  project + ".json")
