# -*- coding:utf-8 -*-
from handler.login.urls import  url as index_url
from handler.user.urls import url as user_url
from handler.pages.urls import url as pages_url
from handler.essay_manage.urls import url as  essay_url
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
    (r"/", index_url),
    (r"/user", user_url),
    (r"/e", essay_url),
    (r"", pages_url),
]
url = CreateUrl(raw_url)