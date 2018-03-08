#!/usr/bin/python
# -*- coding: utf-8 -*-

# from user_handlers import LoginHandle, LogoutHandle, PcGetCaptchaHandler, DemoHandler, DemoLoginHandler
# from user_handlers import LoginHandle
# from password_handlers import ModifyPasswordHandler

# url = [
#     (r"/login", LoginHandle),
    # (r"/logout", LogoutHandle),
    # (r"/geetest/register", PcGetCaptchaHandler),
    # (r"/password/modify", ModifyPasswordHandler),
    # (r'/demo_login', DemoLoginHandler),
    # (r'/demo_page', DemoHandler),
# ]
from user_handlers import DemoLoginHandler,UserLoginHandler


url = [
    (r"/login",DemoLoginHandler),
    (r"/user", UserLoginHandler),

]
