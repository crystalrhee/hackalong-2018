#!/usr/local/bin/python3
from urllib.parse import urlparse
from urllib import request
from urllib.error import HTTPError
from multiprocessing.dummy import Pool
import json
import csv

OUTFILE = 'readmes.csv'
TOKEN = '0ede7d6f422336298bf19dc7ff8656c0260a7438'
STATE = 'state'

def getReadmeFromUrl(repo_url):
    obj = urlparse(repo_url)
    names = ['README', 'readme']
    extensions = ['', '.txt', '.md']
    for name in names:
        for extension in extensions:
            readme_url = 'https://raw.githubusercontent.com{path}/master/{name}{ext}'.format(path=obj.path,
                                name=name,
                                ext=extension)
            try:
                readme = request.urlopen(readme_url).read().decode('utf-8')
                return readme
            except HTTPError:
                pass

def writeReadmeToCsvFromUrl(repo_url):
    print(repo_url)
    writer.writerow([repo_url, json.dumps(getReadmeFromUrl(repo_url))])

def runMultiple(repo_urls, outfile, threads=2):
    pool = Pool(threads)
    pool.map(writeReadmeToCsvFromUrl, repo_urls)
    outfile.flush()
    pool.close()
    pool.join()

prev_id = 1
writer = None

if __name__ == '__main__':
    with open(OUTFILE, 'a') as outfile:
        with open(STATE, 'w+') as state:
            s = state.read()
            if s:
                prev_id = int(s)
        writer = csv.writer(outfile)
        while True:
            try:
                url = 'https://api.github.com/repositories?access_token={}&since={}'.format(TOKEN, prev_id)
                with request.urlopen(url) as response:
                    print('====== downloading', prev_id, '======')
                    page = response.read().decode('utf-8')
                    arr = []
                    for o in json.loads(page):
                        html = o['html_url']
                        arr.append(html)
                        prev_id = o['id']
                    runMultiple(arr, outfile, 8)
                    with open(STATE, 'w') as state:
                        state.write(str(prev_id))
            except Exception as e:
                print(e)
                pass

