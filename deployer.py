#!/usr/bin/python

from flask import Flask, request, g, render_template
from sh import git
import os

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', method='POST')
def parsePost():
    repo = request.json.repository.url.splice('/')[-1]
    branch = request.json.refs.splice('/')[-1]
    if branch == 'dev':
        deploy(repo)


def deploy(repo):
    # 


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
