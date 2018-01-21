import csv
from urllib.parse import urlparse, urlencode, urlunparse
import requests as req

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
    'maxResuts': 1000
}

def getProjectIssues(project_id, startAt = 0):
    args['project'] = project_id
    args['startAt'] = startAt
    urlbits[4] = urlencode(args)
    print(urlunparse(urlbits))
    resp = req.get(urlunparse(urlbits))
    j = resp.json()
    if j['total'] > j['maxResults'] + j['startAt']:
        return j['issues'].append(getProjectIssues(project, j['maxResults'] + j['startAt'] + 1))

with open('jira-projects.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        project = row[0]
        project_id = parseUrl(row[1])
        issues = getProjectIssues(project_id)
        json.dump({project: issues}, "jira_issues/" +  project + ".json")