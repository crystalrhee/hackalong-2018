#!/usr/local/bin/python3
from urllib.parse import urlparse
from urllib import request
from urllib.error import HTTPError
from multiprocessing.dummy import Pool
import json
import csv

OUTFILE = 'repo-contents.csv'
TOKEN = '72b700049e7acda343efafd1b9701bc4758bb01d'

def getReadmeFromUrl(repo_url):
    print(repo_url)
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
                writer.writerow([repo_url, json.dumps(readme)])
            except HTTPError:
                pass

def runMultiple(repo_urls, outfile, threads=2):
    pool = Pool(threads)
    pool.map(getReadmeFromUrl, repo_urls)
    outfile.flush()
    pool.close()
    pool.join()

prev_id = 1
writer = None
count = 1

with open(OUTFILE, 'w') as outfile:
    writer = csv.writer(outfile)
    while True:
        try:
            url = 'https://api.github.com/repositories?access_token={}&since={}'.format(TOKEN, prev_id)
            with request.urlopen(url) as response:
                page = response.read().decode('utf-8')
                arr = []
                for o in json.loads(page):
                    html = o['html_url']
                    arr.append(html)
                    prev_id = o['id']
                    count += 1
                print('====== downloading', count, '======')
                runMultiple(arr, outfile, 8)
        except Exception as e:
            print(e)
            pass

