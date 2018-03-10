# coding: utf-8

from base_handler import BaseHandler, permission
from tornado.web import authenticated
from tornado.gen import coroutine
import hashlib
from database.motor.base import BaseMotor
from config import MongoBasicInfoDb, PERMISSION_NAME_COLLECTION, USER_NAME_COLLECTION, ADMIN_SALT


class ModifyPasswordHandler(BaseHandler):
    @authenticated
    @coroutine
    def post(self):
        if self.get_session('user_type') != '主账号':
            self.set_header('Content-type', 'application/javascript')
            self.write('alert("对不起，只有主账号才有此权限");')
            return
        user_name = self.get_session('main_account_email')
        old_pwd = self.get_argument("old_password")
        new_pwd = self.get_argument("new_password")
        if old_pwd is None or new_pwd is None:
            self.write_response("", 0, "缺少必要的参数")
            return
        mongo_cli = BaseMotor().client
        user_coll = mongo_cli[MongoBasicInfoDb][USER_NAME_COLLECTION]
        user_doc = yield user_coll.find_one({"_id": user_name})
        md5_old_pwd = hashlib.md5(old_pwd + ADMIN_SALT).hexdigest()
        if md5_old_pwd != user_doc.get("password"):
            self.write_response("", 0, "旧密码验证失败")
            return
        md5_new_pwd = hashlib.md5(new_pwd + ADMIN_SALT).hexdigest()
        res = yield user_coll.update_one(
            {"_id": user_name},
            {
                "$set":{
                    "password": md5_new_pwd
                }
            }

        )
        if res.raw_result['updatedExisting'] and res.raw_result["ok"]:
            self.set_header('Content-type', 'application/javascript')
            self.write('alert("修改成功");location.href="/"')
        else:
            self.write_response("", 0, "修改失败")

