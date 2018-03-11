# -*- coding: utf-8 -*-\
import hashlib
from base_handler import BaseHandler
from tornado.gen import coroutine,Return
from tornado.web import authenticated

from config import GT_ID,GT_KEY,ADMIN_SALT,MongoBasicInfoDb,PERMISSION_NAME_COLLECTION
from geetest import GeetestLib
import logging
from log import *
from models.account import Account,AccountNotExistError
from libs.motor.base import BaseMotor

class CmsIndexHandler(BaseHandler):
    @coroutine
    def get(self):
        self.render('cms/base.html')



class LoginHandler(BaseHandler):
    @coroutine
    def get(self):
        next_url = self.get_argument('next', '/cms/')
        self.set_cookie('_xsrf',self.xsrf_token)
        msg = ''
        if next_url == '/user/logout':
            next_url = '/cms/'
        self.render("cms/user_login.html",msg = msg,next_url=next_url)

    @coroutine
    def post(self):
        next_url = self.get_argument('next', '/cms/')
        try:
            gt = GeetestLib(GT_ID, GT_KEY)
            challenge = self.get_argument(gt.FN_CHALLENGE, "")
            validate = self.get_argument(gt.FN_VALIDATE, "")
            seccode = self.get_argument(gt.FN_SECCODE, "")
            status = int(self.session[gt.GT_STATUS_SESSION_KEY])
            user_id = self.session["user_id"]
            if status:
                verify_res = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                verify_res = gt.failback_validate(challenge, validate, seccode)
                self.session["user_id"] = user_id
            if verify_res:
                user_email = self.get_argument('user_email')
                try:
                    subaccount_id = self.get_argument('sub_account')
                    if subaccount_id == '':
                        subaccount_id = None
                except:
                    subaccount_id = None
                password = self.get_argument('password')
                password = hashlib.md5(password + ADMIN_SALT).hexdigest()
                try:
                    account = Account(user_email, subaccount_id)
                    if not account.status:
                        self.clear_session_obj()
                        msg = "账户被禁用"
                        self.render("cms/user_login.html", msg=msg, next_url=next_url)
                        return
                    main_account = Account(user_email)
                except AccountNotExistError:
                    self.clear_session_obj()
                    msg = "账户不存在"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
                    return
                except Exception as e:
                    logging.exception(e)
                    print e
                    msg = "系统错误"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
                    return
                if account.document.get("password") == password:
                    # 密码正确
                    if account.is_main_account and account.document.get("permission") == "super_admin":
                        permision = {'status': True}
                    else:
                        permision = yield self.getPermission(user_email, subaccount_id)

                    if permision['status']:
                        self.session['raw_permission'] = account.document.get("permission")
                        self.session['user_type'] = '主账号' if account.is_main_account else '子账号'
                        self.session['user_name'] = account.document.get("user_name")
                        self.session['permission'] = permision
                        self.session['sub_account'] = subaccount_id
                        self.session["role"] = account.role
                        self.session['main_account_email'] = user_email
                        self.set_secure_cookie("user", user_email + subaccount_id if subaccount_id else user_email,
                                               expires_days=1)
                        # 登录成功！
                        self.redirect(next_url)
                        return
                    else:
                        self.clear_session_obj()
                        msg = '获取权限分组异常'
                        self.render("cms/user_login.html", msg=msg, next_url=next_url)
                        return
                else:
                    self.clear_session_obj()
                    msg = "账号或密码错误"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
            else:
                self.clear_session_obj()
                msg = '验证码验证失败，请重新验证'
                self.render("cms/user_login.html", msg=msg, next_url=next_url)
        except Exception as e:
            logging.exception(e)
            msg = '登录出现异常，请稍后重试'
            print e
            self.render("cms/user_login.html", msg=msg, next_url=next_url)

    @coroutine
    def getPermission(self, main_account, subaccount_id):
        collection = BaseMotor().client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]
        result = yield collection.find_one({'_id': str(main_account)})
        if result is None:
                raise Return({'status': False, 'err_msg': '账号不存在'})
        if result.get(subaccount_id):
            result[subaccount_id]['status'] = True
            raise Return(result[subaccount_id])
        else:
            raise Return({"status": False})




class PcGetCaptchaHandler(BaseHandler):
    @coroutine
    def get(self):
        user_id = 'test'
        try:
            gt = GeetestLib(GT_ID, GT_KEY)
            status = gt.pre_process(user_id)
            self.session[gt.GT_STATUS_SESSION_KEY] = str(status)
            self.session["user_id"] = user_id
            response_str = gt.get_response_str()
            self.write(response_str)
        except Exception as e:
            logging.exception(e)
            self.write('对不起，请求验证码异常')


class LogoutHandler(BaseHandler):
    # 登陆认证
    @coroutine
    def get(self, *args, **kwargs):
        try:
            self.clear_all_cookies()
            msg = '安全退出成功，请重新登录'
        except Exception as e:
            print e
        self.render("cms/user_login.html", msg=msg, next_url='/cms/login')