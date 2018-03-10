# coding: utf-8
import json
import tornado.gen
from base_handler import BaseHandler
from base_handler import permission, is_main_account
from tornado.web import authenticated
from database.motor.base import BaseMotor
from config import MongoBasicInfoDb, ServerPortCollection
from utils.tools import to_string


permission_list = ['traffic', 'tenantManage', 'subAccountManage', 'loadBalance', 'tokenManage', 'defendIp', 'multilineManage', 'switchManage', 'businessManage', 'resourceManage', 'idcUserPage']


class TopoHandler(BaseHandler):
    @tornado.gen.coroutine
    @authenticated
    @permission('traffic', 'r')
    def get(self):
        args = {
            "title": "机房拓扑图",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount":True if self.get_session('user_type') == '主账号' else self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("topo.html", **args)


class TenantOverviewHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('traffic', 'r')
    def get(self):
        args = {
            "title": "租户总览",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("tenant_page.html", **args)


class TenantManageHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('tenantManage', 'r')
    def get(self):
        args = {
            "title": "租户管理",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("tenant_manage.html", **args)


class IpDetailHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('traffic', 'r')
    def get(self):
        args = {
            "title": "ip详情",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::"  + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission')),
        }
        self.render("ip_detail.html", **args)


class IpGroupDetailHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('traffic', 'r')
    def get(self):
        args = {
            "title": "ip组详情",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::"  + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("ip_group_detail.html", **args)


class IpHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('traffic', 'r')
    def get(self):
        coll = BaseMotor().client[MongoBasicInfoDb][ServerPortCollection]
        res = yield coll.find().to_list(length=1000)
        if res:
            for i in res:
                i.pop('_id')
        args = {
            "title": "ip总览",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission')),
            'ports': res
        }
        self.render("ip_page.html", **args)


class TenantDetailHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('traffic', 'r')
    def get(self):
        args = {
            "title": "租户详情",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("tenant_detail.html", **args)


class SwitchManageHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('switchManage', 'r')
    def get(self):
        args = {
            "title": "交换机管理",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("switch_manage.html", **args)


class SwitchDetailHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('switchManage', 'r')
    def get(self):
        args = {
            "title": "交换机详情",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("switch_detail.html", **args)


class SwitchDetailPortHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('switchManage', 'r')
    def get(self):
        args = {
            "title": "交换机端口详情",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("port_detail.html", **args)


class SubAccountHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('subAccountManage', 'r')
    def get(self):
        args = {
            "title": "子账户管理",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email")+"::" + self.get_session("sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("subAccount.html", **args)


class ModifyPasswordHandler(BaseHandler):
    @authenticated
    @is_main_account
    @tornado.gen.coroutine
    def get(self):
        if self.get_session('user_type') != '主账号':
            self.write('<script>alert("对不起，只有主账号才有此权限");history.back()</script>')
            return
        args = {
            "title": "修改主账户密码",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email") + "::" + self.get_session(
                "sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("modify_password.html", **args)


class IndexViewHandler(BaseHandler):

    @authenticated
    @tornado.gen.coroutine
    def get(self):
        args = {
            "title": "机房拓扑图",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email") + "::" + self.get_session(
                "sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        # h = return_first_permission_page(args['permission'])
        if self.get_session('role') == '管理':
            self.render("topo.html", **args)
        else:
            self.render("business_manage/to_do_work_order.html", **args)


class IdcSystemHandler(BaseHandler):
    """
    IDC样式/logo/站点名称修改
    """
    @authenticated
    @permission('idcUserPage', 'r')
    @tornado.gen.coroutine
    def get(self):
        args = {
            "title": "用户页面管理",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email") + "::" + self.get_session(
                "sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "idc_info": {
                "selected_idc": (self.get_session("idc"), self.get_session("idc_name")),
                "idcs": self.get_session("idcs")
            },
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("idc_user_modify.html", **args)


def get_page_permission(permission_session):
    data = []
    if not isinstance(permission_session, dict):
        permission_session = json.loads(permission_session)
    for key in permission_session:
        if key in permission_list:
            if permission_session[key]['r']:
                data.append(to_string(key))
    return data


def return_first_permission_page(list):
    for p in permission_list:
        if to_string(p) in list:
            if p == 'traffic':
                return 'topo.html'
            elif p == 'tenantManage':
                return 'tenant_manage.html'
            elif p == 'loadBalance':
                return 'load_balance_page.html'
            elif p == 'tokenManage':
                return 'token_manage.html'
            elif p == 'defendIp':
                return 'defend_ip_page.html'
            elif p == 'multilineManage':
                return 'multiline_page.html'
            elif p == 'switchManage':
                return 'configuring_switch/port_index.html'
            elif p == 'businessManage':
                return 'business_manage/role_group_manage.html'
            elif p == 'resourceManage':
                return 'business_manage/resource_collection.html'
            elif p == 'idcUserPage':
                return 'idc_user_modify.html'
