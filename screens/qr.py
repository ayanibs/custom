import customtkinter
from PIL import Image
import os


class QRFrame(customtkinter.CTkFrame):
    def __init__(self, master, proceed_to_login=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.proceed_to_login_callback = proceed_to_login

        # Paths
        current_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_path, "..", "assets")
        qr_path = os.path.join(assets_path, "qr.png")
        logo_path = os.path.join(assets_path, "logo.png")

        # Main QR frame (left side, solid color, blue border)
        self.qr_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=3)
        self.qr_frame.place(relx=0.08, rely=0.15, relwidth=0.45, relheight=0.7)

        # QR image (centered vertically)
        self.qr_img = customtkinter.CTkImage(Image.open(qr_path), size=(200, 200))
        self.qr_label = customtkinter.CTkLabel(self.qr_frame, image=self.qr_img, text="")
        self.qr_label.pack(pady=(0, 20), expand=True)  # expand centers it vertically

        # Scan instruction (below QR image)
        self.scan_label = customtkinter.CTkLabel(
            self.qr_frame, text="Scan your Student ID QR code",
            font=customtkinter.CTkFont(size=16)
        )
        self.scan_label.pack(pady=(0, 30))

        # Login button (bottom, with space)
        self.login_button = customtkinter.CTkButton(
            self.qr_frame, text="LOGIN", width=200, height=40,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            command=self.proceed_to_login
        )
        self.login_button.pack(pady=(0, 40))

        # Logo and text (right side)
        self.logo_img = customtkinter.CTkImage(Image.open(logo_path), size=(250, 250))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo_img, text="")
        self.logo_label.place(relx=0.7, rely=0.21)

        self.vitalsense_label = customtkinter.CTkLabel(
            self, text="VITALSENSE",
            font=customtkinter.CTkFont(size=45, weight="bold", family="Helvetica")
        )
        self.vitalsense_label.place(relx=0.7, rely=0.65)

    def proceed_to_login(self):
        print("Login button pressed")  # Debug
        self.master.show_login_page()

