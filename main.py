import customtkinter

# Set the midnight theme before anything else
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("assets/midnight.json")

from app import KioskApp

if __name__ == "__main__":
    app = KioskApp()
    app.mainloop()