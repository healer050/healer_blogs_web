#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import MongodbHost, MongodbPort, MongodbUser, MongodbPassword, MongoBasicInfoDb, IDC_COLLECTION
from influxtor import InfluxDBClient
from tornado.gen import coroutine, Return
from database.motor.base import BaseMotor


class BaseInfluxtor(object):

    def __init__(self,idc):
        self.idc = idc

    @coroutine
    def get_idc_influxdb_info(self, idc=None):
        idc = idc or self.idc
        mongo_client = BaseMotor().client
        idc_info = yield mongo_client[MongoBasicInfoDb][IDC_COLLECTION].find_one({"_id":idc})
        if not idc_info:
            raise NameError("No idc named %s" %idc)
        idc_influxdb_info = {
            "host": idc_info.get('influxdb_host').encode("utf-8"),
            "port": int(idc_info.get('influxdb_port')),
            "username": idc_info.get('influxdb_username').encode("utf-8"),
            "password": idc_info.get('influxdb_password').encode("utf-8"),
            "database": idc_info.get('influxdb_database').encode("utf-8"),
            "ssl": idc_info.get('influxdb_ssl'),
            "verify_ssl": idc_info.get('influxdb_verify_ssl')
        }
        raise Return(idc_influxdb_info)

    @coroutine
    def get_client(self):
        idc_influxdb_info = yield self.get_idc_influxdb_info()
        client = InfluxDBClient(** idc_influxdb_info)
        raise Return(client)

    @coroutine
    def query(self,query):
        client = yield self.get_client()
        result = yield client.query(query)
        raise Return(result)
