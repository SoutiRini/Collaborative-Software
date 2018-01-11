from pyquery import PyQuery as pq
import urllib.request

root = 'http://mail-archives.apache.org/mod_mbox'
project = 'cordova-dev'

d = pq(root + '/' + project)

months = [x.attr('href').split('/')[0] for x in d('.year td a').items() if x.text() == 'Date']

for month in months:
    response = urllib.request.urlopen(root + '/' + project + '/' + month)
    with open('data/' + month, 'wb') as f:
        f.write(response.read())


#http://mail-archives.apache.org/mod_mbox/cordova-dev/201801.mbox/raw/%3c166866877.869.1514775098330.JavaMail.jenkins@jenkins-master.apache.org%3e
#http://mail-archives.apache.org/mod_mbox/cordova-dev/201801.mbox/%3c166866877.869.1514775098330.JavaMail.jenkins@jenkins-master.apache.org%3e
