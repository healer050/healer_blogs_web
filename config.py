# -*- coding: utf-8 -*-

import os
from local_config import *



PORT = 8050
DEBUG = True
BIND_IP = "127.0.0.1"

MONGO_USE_RS = True
MONGO_RS_HOST_PORT = [
    ("127.0.0.1", 27017)
]

MongodbHost = '127.0.0.1'
MongodbPort = 27017
MongodbAuthDb = "admin"
MongodbUser = ''
MongodbPassword = ''
MongoBasicInfoDb = "BasicInfo"
USER_NAME_COLLECTION = 'user'
PERMISSION_NAME_COLLECTION = 'permission'
OPEN_ID_COLLECTION = "open_id"
BULLETIN_INFOS = "bulletin_infos"


permission_list = ['subAccountManage', 'businessManage', 'resourceManage', ]



GT_ID = "80ae976be97d4b56ab1ab05d8ed89546"
GT_KEY = "ec83a1fe5b0031515024b0c89dd72ba5"
ASE_KEY = "37c8e37531ab907b845e9ca5"

setting = {
    "cookie_secret": COOKIE_SECRET,
    "login_url": "/login",
    "xsrf_cookies": False,
    'gzip': True,
    'debug': DEBUG,
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    # pycket的配置信息
    'pycket':PYCKET,
}

try:
    from local_config import *
except ImportError:
    pass

