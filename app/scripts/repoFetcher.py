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
    '''Grabs the readme string data and write to file.
    Agrs:
        repo_url: url of the repo
    '''
    print(repo_url)
    writer.writerow([repo_url, json.dumps(getReadmeFromUrl(repo_url))])

def runMultiple(repo_urls, outfile, threads=2):
    '''Start the thread pool to download/write readmes.
    Args:
        repo_urls: list of repo urls
        outfile: reference to a file object
        threads: number of threads to use
    '''
    pool = Pool(threads)
    pool.map(writeReadmeToCsvFromUrl, repo_urls)
    outfile.flush()
    pool.close()
    pool.join()

if __name__ == '__main__':
    with open(config['output'], 'a') as outfile:
        # state keeps track of the current/previous repo ID (begins from 1)
        with open(config['state'], 'r') as state:
            s = state.read()
            if s:
                prev_id = int(s)
        writer = csv.writer(outfile)
        # Each iteration will fetch about 364 readmes because each api request returns that much (by defaut)
        while True:
            try:
                # using an access token allows to make 5000 requests per hour (2018/08/14)
                url = 'https://api.github.com/repositories?access_token={}&since={}'.format(config['token'], prev_id)
                with request.urlopen(url) as response:
                    print('====== downloading', prev_id, '======')
                    page = response.read().decode('utf-8')
                    repo_links = []
                    for o in json.loads(page):
                        html = o['html_url']
                        repo_links.append(html)
                        prev_id = o['id']
                    try:
                        runMultiple(repo_links, outfile, 12)
                        # stores the state every ~364 repos being downloaded
                        # Note: this implementation will not re-download each failed download or check for duplicates,
                        #       it will simply resume at the previous N * 364'th ID and potentially have duplicates in the output
                        with open(config['state'], 'w') as state:
                            state.write(str(prev_id))
                    except Exception as e:
                        print(e)
                        pass
            except Exception as e:
                print(e)
                pass
