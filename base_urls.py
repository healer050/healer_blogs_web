# -*- coding:utf-8 -*-
from handler.login.urls import  url as login_url
from handler.user.urls import url as user_url
def CreateUrl(raw_url):
    url = []
    for i in raw_url:
        if isinstance(i[1], list):
            for j in i[1]:
                url.append((r"%s" % i[0]+j[0], j[1]))
        else:
            url.append(i)
    return url

raw_url = [
    (r"/", login_url),
    (r"/user", user_url),
]
url = CreateUrl(raw_url)