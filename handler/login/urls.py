from handler import Handler,LoginHandler,DemoLoginHandler


url = [
    (r"/index", Handler),
    (r"login",LoginHandler),
    (r"d/login",DemoLoginHandler),

]
