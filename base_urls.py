# -*- coding:utf-8 -*-
from handler.cms.cms_handlers import CmsIndexHandler,LoginHandler,PcGetCaptchaHandler,LogoutHandler
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
    (r"/cms/",CmsIndexHandler),
    (r"/cms/login",LoginHandler),
    (r"/cms/geetest/register",PcGetCaptchaHandler),
    (r"/cms/logout",LogoutHandler),
]
url = CreateUrl(raw_url)