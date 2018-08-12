from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlparse

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
