import config
import csv
import json
from multiprocessing.dummy import Pool
from urllib import request

from githubWrapper import getReadmeFromUrl, getPublicRepos

prev_id = 1
writer = None

def writeReadmeToCsvFromUrl(repo_url):
    '''Grabs the readme string data and write to file.
    Agrs:
        repo_url: url of the repo
    '''
    print(repo_url)
    readme = getReadmeFromUrl(repo_url)
    if readme:
        writer.writerow([repo_url, json.dumps(readme)])

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

def restoreState():
    try:
        # found the previous state/id, use that
        state = open(config.STATE, 'r')
        s = state.read()
        return int(s) if s else 1
    except:
        # file doesn't exist or bad state content, create a new state
        state = open(config.STATE, 'w')
        return 1

if __name__ == '__main__':
    with open(config.READMES, 'a') as outfile:
        writer = csv.writer(outfile)
        # state keeps track of the current/previous repo ID (begins from 1)
        prev_id = restoreState()
        try:
            failure_count = 0
            while True:
                try:
                    # Each iteration will fetch about 364 readmes because each api request returns that much (by defaut)
                    print('====== downloading', prev_id, '======')
                    repo_links, prev_id = getPublicRepos(prev_id)
                    try:
                        runMultiple(repo_links, outfile, 12)
                        # stores the state every ~364 repos being downloaded
                        # Note: this implementation will not re-download each failed download or check for duplicates,
                        #       it will simply resume at the previous N * 364'th ID and potentially have duplicates in the output
                        with open(config.STATE, 'w') as state:
                            state.write(str(prev_id))
                    except Exception as e:
                        print(e)
                        pass
                except Exception as e:
                    failure_count += 1
                    print(e)
                    if failure_count >= 20:
                        print('Too many failures, gonna give up now, kthxbai')
                        exit()
                    pass
        finally:
            state.close()
