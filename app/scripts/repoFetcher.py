#!/usr/local/bin/python3
from urllib import request
from multiprocessing.dummy import Pool
from githubWrapper import getReadmeFromUrl
from config import RepoFetcher as config
import json
import csv

prev_id = 1
writer = None

def writeReadmeToCsvFromUrl(repo_url):
    print(repo_url)
    writer.writerow([repo_url, json.dumps(getReadmeFromUrl(repo_url))])

def runMultiple(repo_urls, outfile, threads=2):
    pool = Pool(threads)
    pool.map(writeReadmeToCsvFromUrl, repo_urls)
    outfile.flush()
    pool.close()
    pool.join()

if __name__ == '__main__':
    with open(config['output'], 'a') as outfile:
        with open(config['state'], 'w+') as state:
            s = state.read()
            if s:
                prev_id = int(s)
        writer = csv.writer(outfile)
        while True:
            try:
                url = 'https://api.github.com/repositories?access_token={}&since={}'.format(config['token'], prev_id)
                with request.urlopen(url) as response:
                    print('====== downloading', prev_id, '======')
                    page = response.read().decode('utf-8')
                    arr = []
                    for o in json.loads(page):
                        html = o['html_url']
                        arr.append(html)
                        prev_id = o['id']
                    runMultiple(arr, outfile, 8)
                    with open(config['state'], 'w') as state:
                        state.write(str(prev_id))
            except Exception as e:
                print(e)
                pass
