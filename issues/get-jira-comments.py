import json
import os
from random import randint
from time import sleep
from multiprocessing import Pool
from stem.control import Controller
from stem.process import launch_tor_with_config
from stem import Signal
import requests
import threading
import shutil

issueFolder = 'jira_issues'
comment_folder = 'jira_comments'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}

def getForProject(path):
    proxyPort = randint(10000, 20000)
    controlPort = proxyPort + randint(1,10000)
    tid = randint(1, 55053)
    data_dir = '~/.tor/data' + str(tid) + '/'
    print('Opening tor at proxy port ' + str(proxyPort) + ' and control port ' + str(controlPort))
    shutil.copytree(os.path.expanduser('~/.tor/template/'), os.path.expanduser(data_dir))
    tor_proc = launch_tor_with_config(config=
        {
            'SocksPort': str(proxyPort),
            'ControlPort': str(controlPort),
            'DataDirectory': data_dir
        }, take_ownership=True)
    print("Tor opened successfully")
    ctrl = Controller.from_port(port=controlPort)
    ctrl.authenticate(password=None)
    session = requests.Session()
    session.proxies.update({
        'http': 'socks5://localhost:{}'.format(proxyPort),
        'https': 'socks5://localhost:{}'.format(proxyPort),
    })
    print('Processing ' + os.path.basename(path))
    fullIssues = []
    with open(path, 'r') as f:
        issues = json.load(f)
        issues = [x for sublist in issues for x in sublist] # flattening
        for issue in issues:
            url = issue['self']
            print('Getting ' + url)
            count = 1
            while count <= 3:
                try:
                    resp = session.get(url, headers=headers)
                    break
                except:
                    print("Something went wrong. Trying again (" + str(count) + "/3)...")
                    sleep(randint(1,10))
                    ctrl.signal(Signal.NEWNYM)
                    count = count + 1
            j = resp.json()
            fullIssues.append(j)
            sleep(randint(1,10))
            ctrl.signal(Signal.NEWNYM)

    session.close()
    ctrl.close()
    tor_proc.terminate()
    shutil.rmtree(data_dir)

    with open(os.path.join(comment_folder, os.path.basename(path)), 'w') as f:
        json.dump(fullIssues, f)

if __name__ == '__main__':
    p = Pool(16)
    p.map(getForProject, [entry.path for entry in os.scandir(issueFolder) if entry.is_file()])
