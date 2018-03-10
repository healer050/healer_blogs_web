from handler import Handler,LoginHandler,DemoLoginHandler


url = [
    (r"*", Handler),
    (r"login",LoginHandler),
    (r"d/login",DemoLoginHandler),

]
