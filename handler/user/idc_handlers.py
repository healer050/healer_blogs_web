# coding: utf-8

from base_handler import BaseHandler
from tornado.web import authenticated
from tornado.gen import coroutine
from database.motor.base import BaseMotor
from config import MongoBasicInfoDb, PERMISSION_NAME_COLLECTION, USER_NAME_COLLECTION
from models.account import Account
from log import *
#

class SelectIdcHandler(BaseHandler):
    @authenticated
    @coroutine
    def post(self):
        try:
            idc = self.get_argument("idc", None)
            if idc is None:
                self.write_response({}, 0, "参数错误")
            permission_coll = BaseMotor().client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]
            user_coll = BaseMotor().client[MongoBasicInfoDb][USER_NAME_COLLECTION]
            permission = yield permission_coll.find_one({'_id': str(idc)})
            user_info = user_coll.find_one({"_id": self.get_session("main_account_email")})
            if permission is None:
                permission = yield permission_coll.find_one({'_id': "General"})
                if permission is None:
                    self.write_response({}, 0, "缺少该机房权限信息")
                    return
            user_info = yield user_info
            if user_info is None:
                self.clear_session_obj()
                self.write_response({}, 0, "登录状态异常，请重新登录")
                return
            idcs = user_info.get("idcs", [])
            if not (idc in idcs and idc in [c[0] for c in self.get_session("idcs")]):
                self.write_response({}, 0, "该机房不存在，如果您确认操作合法，请重新登录后再尝试")
                return
            idc_tuple = None
            for idc_tp in self.get_session("idcs"):
                if idc == idc_tp[0]:
                    idc_tuple = idc_tp
                    break
            if not idc_tuple:
                raise IndexError

            current_account = Account(self.get_session("main_account_email"), self.get_session("sub_account"))
            if current_account.is_main_account and current_account.document.get("permission") == "super_admin":
                permission = {'status': True}
            else:
                permission = permission.get(current_account.permission)
            if permission is None:
                self.write_response("", 0, "账号权限有误")
                return
            self.set_session("idc", idc_tuple[0])
            self.set_session("idc_name", idc_tuple[1])
            self.set_session("permission", permission)
            self.write_response("切换机房成功")
        except Exception as e:
            logging.exception(e)
            self.write_response({}, 0, "出错了")

