

import requests
from bs4 import BeautifulSoup

GITHUB = 'https://github.com'
TRENDING_URL = GITHUB + "/trending"
TRENDING_DEV_URL = TRENDING_URL + "/developers"

USER_AGENT_BY_MOBILE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36 PostmanRuntime/7.29.2'

# def get_trending_repos(opts):
#     repos = []

#     language = opts.get('language', None)
#     since = opts.get('since', None)

#     url = TRENDING_URL

#     if language:
#         url = url + '/' + language

#     if since:
#         url += '?since={}'.format(since)

#     response, code = read_page(url)

#     if code == 200:
#         repos = parser_repos(response)

#     return repos


def get_trending_developers(opts):
    developers = []

    language = opts.get('language', None)
    since = opts.get('since', None)

    url = TRENDING_DEV_URL

    if language:
        url = url + '/' + language

    if since:
        url += '?since={}'.format(since)

    print(url)
    response, code = read_page(url)

    if code == 200:
        developers = parser_developers(response)

    return developers


def parser_repos(response):

    repos = []
    print(response.content)
    soup = BeautifulSoup(response.content, "lxml")

    for li in soup.find_all('li', {'class': 'col-12 d-block width-full py-4 border-bottom'}):
        avatar_img = li.find('img', {'class': 'avatar mb-1'})
        if avatar_img:
            avatar = avatar_img['src']

        name_div = li.find('div', {'class': 'd-inline-block col-9 mb-1'})
        name_string = name_div.find('a', href=True)['href']
        # name_string = li.find('span', {'class': 'text-normal'}).string
        owner = name_string.split('/')[1]
        repo = name_string.split('/')[2]
        link = GITHUB + name_string

        meta = li.find('div', {'class': 'f6 text-gray mt-2'})

        if meta:
            stars = li.find('a', {'class': 'muted-link d-inline-block mr-3'}).text.replace('\n', '').strip(' ')
        else:
            stars = "0"

        desc = parser_desc(li.find('div', {'class': 'py-1'}))

        repos.append({
            'owner': owner,
            'avatar': avatar,
            'repo': repo,
            'stars': stars,
            'desc': desc,
            'link': link
        })

    return repos


def parser_desc(desc):
    repo_desc = ""

    if desc:
        for each in desc.stripped_strings:
            repo_desc += " " + each

    return repo_desc.lstrip(" ")


def parser_developers(response):
    developers = []
    
    soup = BeautifulSoup(response.text, "html")
    for li in soup.find_all('li', {'class': 'd-sm-flex flex-justify-between border-bottom border-gray-light py-3'}):
        avatar_img = li.find('img', {'class': 'rounded-1'})['src']
        if avatar_img:
            avatar = avatar_img['src']

        href = li.find('a', {'class': 'd-inline-block'})['href']
        link = GITHUB + href
        name = href[1:]

        developers.append({
            'avatar': avatar,
            'name': name,
            'full_name': "",
            'link': link
        })

    return developers


def parser_developer_name(name):
    full_name = ""
    if name:
        for each in name.stripped_strings:
            full_name += " " + each

    return full_name.lstrip(" ")


def read_page(url):
    # header = {'User-Agent': USER_AGENT_BY_MOBILE}
    try:
        response = requests.get(url=url)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return None, False

    return response, response.status_code