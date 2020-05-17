from urllib import request, parse
import json
import os


def trigger(repository, branch):
    body = {
        "request": {"branch": branch}
    }
    data = json.dumps(body)
    repository = parse.urlencode(repository)
    travis_url = f"https://api.travis-ci.com/repo/{repository}/requests"
    travis_token = os.environ["TRAVIS_TOKEN"]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Travis-API-Version": 3,
        "Authorization": f"token {travis_token}"
    }

    req = request.Request(travis_url, data=data, headers=headers)
    resp = request.urlopen(req)
    resp_body = resp.read()
    return resp_body
