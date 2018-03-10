from base_handler import BaseHandler

class AdminHandler(BaseHandler):

    def get(self):
        self.render("admin_base.html")


