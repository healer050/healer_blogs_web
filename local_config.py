# -*- coding: utf-8 -*-
import uuid,base64
from models.admin_models import CmsUsers
# from libs.db.dbsession import dbSession





#cookie_secret
COOKIE_SECRET = base64.b64encode(uuid.uuid4().bytes)
# pycket的配置信息
PYCKET = {
    'engine': 'redis',  # 设置存储器类型
    'storage': {
        'host': 'localhost',
        'port': 6379,
        'db_sessions': 5,
        'db_notifications': 11,
        'max_connections': 2 ** 31,
    },
    'cookies': {
        'expires_days': 30,  # 设置过期时间
        'max_age': 5000,
    },
}
PORT = 8010
DEBUG = True
BIND_IP = "0.0.0.0"



# 创建超级管理员
def create_super_user():
    cms_user = CmsUsers()
    cms_user.email = "healer@outlook.com"
    cms_user.password = "asdfghjkl"
    # dbSession.add(cms_user)
    # dbSession.commit()