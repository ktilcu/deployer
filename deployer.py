#!/usr/bin/python

from flask import Flask, request
from logging import FileHandler

import os
import logging
import json
import subprocess
import sys

app = Flask(__name__)
app.config.from_object(__name__)

logger = logging.getLogger('deployer')
file_handler = FileHandler('/home/trike/nginx-root/log.txt')
file_handler.setLevel(logging.WARNING)
logger.addHandler(file_handler)


@app.route('/', methods=['POST', 'GET'])
def parsePost():
    payload = json.loads(request.form['payload'])
    repo = payload['repository']['name']
    branch = payload['ref'].split('/')[-1]
    user = payload['pusher']
    userAuthorized = authUser(user)

    if not any(';' in i for i in (repo, branch)) and userAuthorized:
        deploy(repo, branch)
    return 'oh yeah'


def deploy(repo, branch):
    logger.error("Received Communication from Github for repo %s to push branch %s \n" % (repo, branch))
    if not branch == "dev":
        logger.error("We only do dev pushes these days.")
    folder = whatFolder(repo)
    subprocess.call("/home/trike/deploy.sh %s %s %s" % (folder, branch, repo), shell=True)


def whatFolder(repo):
    try:
        f = open('/home/trike/update/edsconf.json', 'r')
        configText = f.read()
        f.close()
        config = json.loads(configText)
    except:
        logger.error('error opening configuration file')
        sys.exit()

    file_groups = config['file-groups']

    folder = ""
    for pres in file_groups:
        configRepo = file_groups[pres].get('repo', "")
        print "found it %s" % configRepo
        if configRepo == repo:
            folder = pres
            break
    return folder


def authUser(user):
    return True


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
