from screens.loginpage import App as LoginPage

class KioskApp:
    def __init__(self):
        self.current_page = None

    def show_login_page(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = LoginPage()
        return self.current_page

    def get_current_page(self):
        return self.current_page