import config
import json
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlparse


def getReadmeFromUrl(repo_url):
    '''Downloads the readme from a github repo url.
    Args:
        repo_url: repo url
    Returns:
        string format of readme
    '''
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

def getApi(api, attrs, have_multi = False):
    '''Generic api request helper for api that return json
        objects/arrays.
    Args:
        api: url of the api (including params)
        attrs: attributes to filter
        have_multi: json object or array
    Returns:
        dict or array(dict) if have_multi=True
    '''
    try:
        out = [] if have_multi else {}
        with request.urlopen(api) as response:
            response = response.read()
            if have_multi:
                for obj in json.loads(response):
                    tmp = {}
                    for attr in attrs:
                        tmp[attr] = obj[attr]
                    out.append(tmp)
            else:
                obj = json.loads(response)
                for attr in attrs:
                    out[attr] = obj[attr]
        return out
    except Exception as e:
        print(api)
        print(e)
        pass

def getRepoInfoFromUrl(url):
    '''Returns basic info of a github repo.
    Args:
        url: url
    Returns:
        json dump of dict
    '''
    url = urlparse(url)
    api1 = ('https://api.github.com/repos{path}'
            '?access_token={token}').format(path=url.path,
                                            token=config.TOKEN)
    api2 = ('https://api.github.com/repos{path}/contributors'
            '?access_token={token}').format(path=url.path,
                                            token=config.TOKEN)
    out = getApi(api1, 
                    ['name', 'description', 'html_url', 'language'],
                    False)
    contributors = getApi(api2,
                    ['login', 'avatar_url'],
                    True)
    out['contributors'] = contributors
    return json.dumps([out])

def getPublicRepos(since_id):
    ''' Returns ~364 public repo urls at a time
    Args:
        since_id: id of the repo to start
    Returns:
        list of repo urls
    '''
    # using an access token allows to make 5000 requests per hour (2018/08/14)
    url = 'https://api.github.com/repositories?access_token={}&since={}'.format(config.TOKEN, since_id)
    try:
        with request.urlopen(url) as response:
            prev_id = since_id
            page = response.read().decode('utf-8')
            repo_links = []
            for o in json.loads(page):
                html = o['html_url']
                repo_links.append(html)
                prev_id = o['id']
            return repo_links, prev_id
    except Exception as e:
        print('unable to fetch public repo information')
        raise e