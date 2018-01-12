from pyquery import PyQuery as pq
import urllib.request
import os

root = 'http://mail-archives.apache.org/mod_mbox'

dataPath = "/Volumes/GoogleDrive/Team Drives/Reflection Distributed Development/data/"
dataPath = os.path.join(dataPath, 'dev-ml')

if not os.path.exists(dataPath):
    os.mkdir(dataPath)

with open('../apache-projects.txt', 'r', encoding='utf-16') as f:
    for project in f:
        project = project.strip();
        projectPath = os.path.join(dataPath, project)
        if not os.path.exists(projectPath):
            os.mkdir(projectPath)

        projUrl = root + '/' + project + '-dev'
        print("GET: " + projUrl)
        d = pq(projUrl)

        months = [x.attr('href').split('/')[0] for x in d('.year td a').items() if x.text() == 'Date']

        for month in months:
            monthUrl = root + '/' + project + '-dev/' + month
            print("GET: " + monthUrl)
            response = urllib.request.urlopen(monthUrl)
            with open(os.path.join(projectPath, month), 'wb') as f:
                f.write(response.read())


#http://mail-archives.apache.org/mod_mbox/cordova-dev/201801.mbox/raw/%3c166866877.869.1514775098330.JavaMail.jenkins@jenkins-master.apache.org%3e
#http://mail-archives.apache.org/mod_mbox/cordova-dev/201801.mbox/%3c166866877.869.1514775098330.JavaMail.jenkins@jenkins-master.apache.org%3e
