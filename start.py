# -*- coding:utf-8 -*-
from tornado import web,ioloop
from config import setting,PORT,BIND_IP
from base_urls import url




def make_app():
    return web.Application(url,**setting)


if __name__ == "__main__":
    app = make_app()
    print "The healer web server starting..."
    app.listen(PORT,BIND_IP)
    ioloop.IOLoop.current().start()

