import customtkinter
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")



# QRFrame is now a frame, not a root window
class QRFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # load and create background image
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                               size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Welcome to VitalSense Kiosk",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        qr_area = customtkinter.CTkLabel(self.login_frame, text="[ QR Scanner Preview Here ]", 
                                        font=("Arial", 16), fg_color="#f1f2f6", width=30, height=15)
        qr_area.grid(row=1, column=0, padx=30, pady=(10, 15))

        self.manual_login_label = customtkinter.CTkLabel(self.login_frame, text="Can't proceed? Login manually.",
                                                        font=customtkinter.CTkFont(size=12, weight="bold"))
        self.manual_login_label.grid(row=2, column=0, padx=25, pady=(0, 15))
        self.proceed_button = customtkinter.CTkButton(self.login_frame, text="Proceed to Login", command=self.proceed_to_login)
        self.proceed_button.grid(row=4, column=0, padx=30, pady=(15, 15))


    def proceed_to_login(self):
        # Switch to login page using the main app
        self.master.show_login_page()

    def exit_fullscreen(self, event=None):
        self.master.destroy()
