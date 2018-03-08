# coding: utf-8
import motor
from config import MongodbHost, MongodbPort, MongodbAuthDb, MongodbUser, MongodbPassword, MONGO_USE_RS, MONGO_RS_HOST_PORT
from urllib import quote
import string


class BaseMotor(object):

    def __init__(self):

        if MONGO_USE_RS:
            host_port = string.join(
                ["{0}:{1}".format(quote(host), quote(str(port))) for host, port in MONGO_RS_HOST_PORT],
                ","
            )
        else:
            host = quote(MongodbHost)
            port = quote(str(MongodbPort))
            host_port = "{0}:{1}".format(host, port)
        username = quote(MongodbUser)
        password = quote(MongodbPassword)
        auth_db = quote(MongodbAuthDb)
        if username and password and auth_db:
            uri = "mongodb://%s:%s@%s/%s" % (quote(username), quote(password), host_port, quote(auth_db))
        else:
            uri = "mongodb://%s" % host_port
        self.client = motor.motor_tornado.MotorClient(uri)






