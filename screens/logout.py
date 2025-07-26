
import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase

class LogoutScreen(customtkinter.CTkFrame):
    def __init__(self, master, logout_callback, student_id=None):
        super().__init__(master)
        self.master = master
        self.student_id = student_id

        # Load and create background image (same as other screens)
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                              size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Create logout frame
        self.logout_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.logout_frame.grid(row=0, column=0, sticky="ns")

        # Thank you message
        self.thank_label = customtkinter.CTkLabel(self.logout_frame,
            text="Thank you for using VITALSENSE!",
            font=customtkinter.CTkFont(size=36, weight="bold"),
            text_color="black"
        )
        self.thank_label.pack(pady=(200, 20))

        # Press anywhere message
        self.press_label = customtkinter.CTkLabel(self.logout_frame,
            text="Press anywhere to continue",
            font=customtkinter.CTkFont(size=18),
            text_color="black"
        )
        self.press_label.pack(pady=10)

        # Log out the student from Supabase Auth if logged in
        try:
            supabase.auth.sign_out()
        except Exception as e:
            print("Logout error:", e)

        # Bind any mouse click event on this frame to the logout_callback
        self.bind("<Button-1>", lambda event: logout_callback())
        for widget in self.winfo_children():
            widget.bind("<Button-1>", lambda event: logout_callback())