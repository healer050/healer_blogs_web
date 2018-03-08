# -*- coding: utf-8 -*-
from constants import ADMIN_IP
import functools

#管理员权限通过IP地址控制，
def admin_ip_list(method):
    @functools.wraps(method)
    def wraps(self, *args, **kwargs):
        if self.request.remote_ip in ADMIN_IP:
            return method(self, *args, **kwargs)
        else:
            self.write("IP地址不在管理员列表中")
    return wraps

#另外的验证方法
def admin_auth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            if self.session.get('ip_address') == self.request.remote_ip:
                return method(self, *args, **kwargs)
            else:
                self.write('ip地址不相符')
        else:
            self.write('很抱歉，用户没有登录，请登录后再试')
    return wrapper


def permission(permission_name, permission_type):
    """
        perimission_type
        w 写
        r 读
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.get_session('raw_permission') == 'super_admin' and self.get_session('user_type') == '主账号':
                return func(self, *args, **kwargs)
            permission_dict = self.get_session('permission')
            if permission_dict is not None:
                if permission_dict.get(permission_name, {}).get(permission_type):
                    return func(self, *args, **kwargs)
                else:
                    # todo 返回无权限的界面
                    if self.request.method == 'GET':
                        self.write('<script>alert("对不起，您可能没有权限访问");history.back()</script>')
                    else:
                        self.set_header('Content-type', 'application/javascript')
                        self.write('alert("对不起，您可能没有权限访问");')
            else:
                login_url = self.get_login_url()
                self.redirect(login_url)
                return
        return wrapper
    return decorator
