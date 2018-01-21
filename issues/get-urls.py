import json

with open('apache-projects.json', 'r') as f:
    projects = json.load(f)
    for project, data in projects.items():
        if('bug-database' in data):
            print(project + ',' + data['bug-database'])
