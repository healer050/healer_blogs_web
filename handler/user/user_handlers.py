# coding: utf-8
from base_handler import BaseHandler

class DemoLoginHandler(BaseHandler):

    def get(self):
        self.render("demo_login.html")
class UserLoginHandler(BaseHandler):

    def get(self):
        self.render("user_login.html")
# from utils import int_to_ip
# from handle_ev import get_list

# import hashlib
# import tornado.gen
# import tornado.web
# from tornado.gen import Return, coroutine
# from tornado.web import authenticated
# from base_handler import BaseHandler
# from config import GT_KEY, GT_ID, ADMIN_SALT, PERMISSION_NAME_COLLECTION, IDC_COLLECTION, MongoBasicInfoDb
# from config import BaseMongodbDb, LoadBalanceCollention
# from database.motor.base import BaseMotor
# from geetest import GeetestLib
# from models.account import Account, AccountNotExistError
# from log import *


# class LoginHandle(BaseHandler):
    # @coroutine
    # def get(self):
        # next_url = self.get_argument('next', '/')
        # self.set_cookie('_xsrf',self.xsrf_token)
        # msg = ''
        # if next_url == '/user/logout':
        #     next_url = '/'
        # self.render("user_login.html",msg = msg,next_url=next_url)
        # self.render("user_login.html")

#     @coroutine
#     def post(self):
#         next_url = self.get_argument('next', '/')
#         try:
#             gt = GeetestLib(GT_ID, GT_KEY)
#             challenge = self.get_argument(gt.FN_CHALLENGE, "")
#             validate = self.get_argument(gt.FN_VALIDATE, "")
#             seccode = self.get_argument(gt.FN_SECCODE, "")
#             status = int(self.session[gt.GT_STATUS_SESSION_KEY])
#             user_id = self.session["user_id"]
#             if status:
#                 verify_res = gt.success_validate(challenge, validate, seccode, user_id)
#             else:
#                 verify_res = gt.failback_validate(challenge, validate, seccode)
#                 self.session["user_id"] = user_id
#             if verify_res:
#                 user_email = self.get_argument('user_email')
#                 try:
#                     subaccount_id = self.get_argument('sub_account')
#                     if subaccount_id == '':
#                         subaccount_id = None
#                 except:
#                     subaccount_id = None
#                 password = self.get_argument('password')
#                 password = hashlib.md5(password + ADMIN_SALT).hexdigest()
#                 try:
#                     account = Account(user_email, subaccount_id)
#                     main_account = Account(user_email)
#                 except AccountNotExistError:
#                     self.clear_session_obj()
#                     msg = "账户不存在"
#                     self.render("user_login.html", msg=msg, next_url=next_url)
#                     return
#                 except Exception as e:
#                     # logging.exception(e)
#                     msg = "系统错误"
#                     self.render("user_login.html", msg=msg, next_url=next_url)
#                     return
#                 if account.document.get("password") == password:
#                     # 密码正确
#                     idcs = account.idcs
#                     idcs_name = self.get_idcs_name(idcs)
#                     if account.is_main_account and account.document.get("permission") == "super_admin":
#                         permision = {'status': True}
#                     else:
#                         permision = yield self.getPermission(user_email, subaccount_id)
#
#                     if permision['status']:
#                         self.session['raw_permission'] = account.document.get("permission")
#                         self.session['user_type'] = '主账号' if account.is_main_account else '子账号'
#                         self.session['user_name'] = account.document.get("user_name")
#                         self.session['permission'] = permision
#                         self.session['version'] = main_account.document.get("product_version")
#                         self.session['sub_account'] = subaccount_id
#                         self.session["role"] = account.role
#                         self.session["group"] = account.group
#                         self.session['main_account_email'] = user_email
#                         idcs_name = yield idcs_name
#                         self.session['idc'] = idcs_name[0][0]
#                         self.session['idc_name'] = idcs_name[0][1]
#                         self.session['idcs'] = idcs_name
#                         self.set_secure_cookie("user", user_email + subaccount_id if subaccount_id else user_email,
#                                                expires_days=1)
#                         # 如果是标准版，把健康检查开关给关掉
#                         try:
#                             if self.session["version"] == "standard":
#                                 for idc in self.session["idcs"]:
#                                     coll = BaseMotor().client[idc[0] + BaseMongodbDb][LoadBalanceCollention]
#                                     tenant_docs = yield coll.find().to_list(length=10000)
#                                     for doc in tenant_docs:
#                                         if doc.get("health_info").get("switch") != "off":
#                                             coll.update_one({
#                                                 "_id": doc.get("_id")
#                                             }, {"$set": {
#                                                 "health_info.switch": "off"
#                                             }})
#                         except:
#                             pass
#                         self.redirect(next_url)
#                         return
#                     else:
#                         self.clear_session_obj()
#                         msg = '获取权限分组异常'
#                         self.render("user_login.html", msg=msg, next_url=next_url)
#                         return
#                 else:
#                     self.clear_session_obj()
#                     msg = "账号或密码错误"
#                     self.render("user_login.html", msg=msg, next_url=next_url)
#             else:
#                 self.clear_session_obj()
#                 msg = '验证码验证失败，请重新验证'
#                 self.render("user_login.html", msg=msg, next_url=next_url)
#         except Exception as e:
#             # logging.exception(e)
#             msg = '登录出现异常，请稍后重试'
#             self.clear_session_obj()
#             self.render("user_login.html", msg=msg, next_url=next_url)
#
#     @coroutine
#     def getPermission(self, main_account, subaccount_id):
#         collection = BaseMotor().client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]
#         result = yield collection.find_one({'_id': str(main_account)})
#         if result is None:
#                 raise Return({'status': False, 'err_msg': '账号不存在'})
#         if result.get(subaccount_id):
#             result[subaccount_id]['status'] = True
#             raise Return(result[subaccount_id])
#         else:
#             raise Return({"status": False})
#
#     @tornado.gen.coroutine
#     def get_idcs_name(self, idcs):
#         idcs_name = []
#         coll = BaseMotor().client[MongoBasicInfoDb][IDC_COLLECTION]
#         for idc in idcs:
#             idcs_name.append(coll.find_one({"_id": idc}))
#         for i in range(len(idcs_name)):
#             idcs_name[i] = (idcs[i], (yield idcs_name[i]).get("name", idcs_name[i]))
#         raise Return(idcs_name)
#
#
# class LogoutHandle(BaseHandler):
#     # 登陆认证
#     @authenticated
#     # 权限认证
#     # @permission('switchManage','r')
#     @tornado.gen.coroutine
#     def get(self, *args, **kwargs):
#         self.clear_session_obj()
#         self.clear_all_cookies()
#         msg = '安全退出成功，请重新登录'
#         self.render("user_login.html", msg=msg, next_url='/')
#
#
# class PcGetCaptchaHandler(BaseHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         user_id = 'test'
#         try:
#             gt = GeetestLib(GT_ID, GT_KEY)
#             status = gt.pre_process(user_id)
#             self.session[gt.GT_STATUS_SESSION_KEY] = str(status)
#             self.session["user_id"] = user_id
#             response_str = gt.get_response_str()
#             self.write(response_str)
#         except Exception as e:
#             # pass
#             # logging.exception(e)
#             self.write('对不起，请求验证码异常')
#
#
# class DemoHandler(BaseHandler):
#     def get(self):
#         self.set_cookie('_xsrf', self.xsrf_token)
#         self.render("demo_login.html")
#
#
# class DemoLoginHandler(LoginHandle):
#     @tornado.gen.coroutine
#     def post(self):
#         try:
#             gt = GeetestLib(GT_ID, GT_KEY)
#             challenge = self.get_argument(gt.FN_CHALLENGE, "")
#             validate = self.get_argument(gt.FN_VALIDATE, "")
#             seccode = self.get_argument(gt.FN_SECCODE, "")
#             status = self.session[gt.GT_STATUS_SESSION_KEY]
#             user_id = self.session["user_id"]
#             if status:
#                 verify_res = gt.success_validate(challenge, validate, seccode, user_id)
#             else:
#                 verify_res = gt.failback_validate(challenge, validate, seccode)
#                 self.session["user_id"] = user_id
#             if verify_res:
#                 user_email = self.get_argument('user_email')
#                 try:
#                     subaccount_id = self.get_argument('sub_account')
#                     if subaccount_id == '':
#                         subaccount_id = None
#                 except:
#                     subaccount_id = None
#                 password = self.get_argument('password')
#                 password = hashlib.md5(password + ADMIN_SALT).hexdigest()
#                 try:
#                     account = Account(user_email, subaccount_id)
#                 except AccountNotExistError:
#                     self.clear_session_obj()
#                     self.render("demo_login.html")
#                     return
#                 except:
#                     self.render("demo_login.html")
#                     return
#                 if account.document.get("password") == password:
#                     # 密码正确
#                     idcs = account.idcs
#                     idcs_name = self.get_idcs_name(idcs)
#                     if account.is_main_account:
#                         permision = {'status': True}
#                     else:
#                         permision = yield self.getPermission(user_email, subaccount_id)
#                     if permision['status']:
#                         self.session['user_type'] = '主账号' if account.is_main_account else '子账号'
#                         self.session['permission'] = permision
#                         self.session['sub_account'] = subaccount_id
#                         self.session["role"] = account.role
#                         self.session['main_account_email'] = user_email
#                         idcs_name = yield idcs_name
#                         self.session['idc'] = idcs_name[0][0]
#                         self.session['idc_name'] = idcs_name[0][1]
#                         self.session['idcs'] = idcs_name
#                         self.set_secure_cookie("user", user_email + subaccount_id if subaccount_id else user_email,
#                                                expires_days=1)
#                         self.redirect('/balance/load_balancing')
#                         return
#                     else:
#                         self.clear_session_obj()
#                         self.render("demo_login.html")
#                         return
#                 else:
#                     self.clear_session_obj()
#                     self.render("demo_login.html")
#             else:
#                 self.clear_session_obj()
#                 self.render("demo_login.html")
#         except Exception as e:
#             pass
#             # logging.exception(e)
#             # self.clear_session_obj()
#             # self.render("demo_login.html")
