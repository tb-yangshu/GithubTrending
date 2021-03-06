#!/usr/bin/env python
# encoding: utf-8

"""
@author: anly_jun
@file: github_trending
@time: 16/10/17 下午2:23
"""
import requests
from bs4 import BeautifulSoup

GITHUB = 'https://github.com'
TRENDING_URL = GITHUB + "/trending"
TRENDING_DEV_URL = TRENDING_URL + "/developers"

USER_AGENT_BY_MOBILE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'


def get_trending_repos(opts):
    repos = []

    language = opts.get('language', None)
    since = opts.get('since', None)

    url = TRENDING_URL

    if language:
        url = url + '/' + language

    if since:
        url += '?since={}'.format(since)

    response, code = read_page(url)

    if code == 200:
        repos = parser_repos(response)

    return repos


def get_trending_developers(opts):
    developers = []

    language = opts.get('language', None)
    since = opts.get('since', None)

    url = TRENDING_DEV_URL

    if language:
        url = url + '/' + language

    if since:
        url += '?since={}'.format(since)

    print url
    response, code = read_page(url)

    if code == 200:
        developers = parser_developers(response)

    return developers


def parser_repos(response):

    repos = []

    soup = BeautifulSoup(response.text, "lxml")

    for div in soup.find_all('div', {'class': 'list-item with-avatar'}):
        avatar = div.find('img', {'class': 'avatar'})['src']
        name_string = div.find('strong', {'class': 'list-item-title'}).string
        owner = name_string.split('/')[0]
        repo = name_string.split('/')[1]
        link = GITHUB + name_string

        meta = div.find('strong', {'class': 'meta'})
        stars = 0

        if meta:
            stars = div.find('strong', {'class': 'meta'}).contents[0].strip('\n').lstrip().rstrip()
        else:
            stars = "0"

        desc = parser_desc(div.find('div', {'class': 'repo-description'}))

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

    soup = BeautifulSoup(response.text, "lxml")
    for div in soup.find_all('div', {'class': 'list-item with-avatar'}):
        avatar = div.find('img', {'class': 'avatar'})['src']
        href = div.find('a')['href']
        full_name = parser_developer_name(div.find('strong', {'class': 'list-item-title'}))
        link = GITHUB + href
        name = href[1:]

        developers.append({
            'avatar': avatar,
            'name': name,
            'full_name': full_name,
            'link': link
        })

    return developers


def parser_developer_name(name):
    full_name = ""
    if name:
        for each in name.stripped_strings:
            full_name += " " + each

    return full_name.lstrip(" ")


def read_page(url, timeout=5):
    header = {'User-Agent': USER_AGENT_BY_MOBILE}
    try:
        response = requests.get(url=url, timeout=timeout, headers=header)
    except requests.exceptions.ConnectionError as e:
        print e
        return None, False

    return response, response.status_code


if __name__ == '__main__':
    response, code = read_page(TRENDING_DEV_URL)

    if code == 200:
        parser_developers(response)

