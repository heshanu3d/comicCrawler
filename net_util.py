# coding:utf-8

import requests

p = {
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080'
}


def requests_get(web_url, retry_num=3, headers=None, proxies=None, decode=None):
    web_content = None
    proxy = None
    if proxies:
        proxy = proxies
    else:
        proxy = p
    try:
        if decode:
            web_content = requests.get(web_url, headers=headers, proxies=proxy).content.decode(decode)
        else:
            web_content = requests.get(web_url, headers=headers, proxies=proxy).content
    except requests.exceptions.ProxyError:
        print('requests.exceptions.ProxyError')
        retry_num -= 1
        if retry_num > 0:
            web_content = requests_get(web_url, retry_num, headers=headers, proxies=proxy, decode=decode)
    except requests.exceptions.ConnectionError:
        print('requests.exceptions.ConnectionError')
        retry_num -= 1
        if retry_num > 0:
            web_content = requests_get(web_url, retry_num, headers=headers, proxies=proxy, decode=decode)
    return web_content
