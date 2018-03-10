from base_handler import BaseHandler

class Handler(BaseHandler):

    def get(self):
        self.render("index.html")


class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

class DemoLoginHandler(BaseHandler):

    def get(self):
        self.render("demo_login.html")
