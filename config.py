# -*- coding: utf-8 -*-

import os
from local_config import *



PORT = 8010
DEBUG = True
BIND_IP = "127.0.0.1"

MONGO_USE_RS = True
MONGO_RS_HOST_PORT = [
    ("192.168.1.149", 27017)
]

MongodbHost = '192.168.1.149'
MongodbPort = 27017
MongodbAuthDb = "admin"
MongodbUser = ''
MongodbPassword = ''
MongoBasicInfoDb = "basicinfo"
USER_NAME_COLLECTION = 'user'
PERMISSION_NAME_COLLECTION = 'permission'
OPEN_ID_COLLECTION = "open_id"
BULLETIN_INFOS = "bulletin_infos"

BaseMongodbDb = '_sdn'
ScanCollection = 'scan'
IpCollection = 'ip'
IpDomainCollection = 'ip_domain'
LinkCollection = 'link'
PortCollection = 'port'
SwitchCollection = "switch"
TenantCollection = "tenant"
LoadBalanceCollention = "load_balance"
IdcSystemCollection = "idcsystem"
IdcUserCollection = "idcuser"
TestCollection = "test"
SshCollection = 'ssh_message'
SourceCollection = "room_resource"
DefendSourceCollecton = "defend_resource"
IDC_COLLECTION = "idc"
COUNT_COLLECTION = "count"
ALARM_COLLECTION = "alarm"
EquipmentEsources = "equipment_resource"
ServerResources = "server_resource"
TokenCollection = 'token'
DefendIpCollection = 'defend_ip'
ServerPortCollection = 'server_port'
BlackWhiteList = 'black_white_list'
LogLevel = "ERROR"
BusinessProcess = "business_process"
ControllerLogFile = 'log/controller.log'
DatabaseLogFile = 'log/db.log'
RestApiLogFile = 'log/rest_api.log'
WorkOrderCollection = 'work_orders'
MachineCabinetCollection = 'machine_cabinet'
ConvergeSwitchCollection = 'converge_switch'
FireWallSetCollection = 'firewall_set'
FormDesignCollection = 'form_design'
ResourceOperationCollection = 'resource_operation'
RentResourceCollection = 'rent_resource'


LOG_DIR = "./log"  # 日志目录
LOG_FILE = 'gh-sdn-web.log'  # 日志文件


ADMIN_SALT = ""
ONE_BUTTON_ONLINE_PWD = ""

GT_ID = "80ae976be97d4b56ab1ab05d8ed89546"
GT_KEY = "ec83a1fe5b0031515024b0c89dd72ba5"
ASE_KEY = "37c8e37531ab907b845e9ca5"

LogLevel = "ERROR"



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

