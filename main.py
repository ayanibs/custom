from app import KioskApp

if __name__ == "__main__":
    kiosk = KioskApp()
    login_page = kiosk.show_login_page()
    login_page.mainloop()