import customtkinter
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Escape>", self.exit_fullscreen)
        self.title("CustomTkinter example_background_image.py")
        self.attributes('-fullscreen', True)  # Set fullscreen
        self.resizable(False, False)
        

        # load and create background image
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                               size=(self.winfo_screenwidth(), self.winfo_screenheight()))
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
        qr_area.grid(row=1, column=0, padx=30, pady=(10, 15))  # Inserted here

        # Corrected line: Use a new variable name and apply grid() to the label
        self.manual_login_label = customtkinter.CTkLabel(self.login_frame, text="Can't proceed? Login manually.",
                                                          font=customtkinter.CTkFont(size=12, weight="bold")) # Adjusted font size for better fit
        self.manual_login_label.grid(row=2, column=0, padx=25, pady=(0, 15)) # Place it before the login button
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def login_event(self):
        print("Login pressed - username:", "password:")

        self.login_frame.grid_forget()  # remove login frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

    def exit_fullscreen(self, event=None):
        self.destroy()  # or self.attributes('-fullscreen', False) to toggle


if __name__ == "__main__":
    app = App()
    app.mainloop()
