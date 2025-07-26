import customtkinter
from PIL import Image
import os

class TemperatureScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, student_id):
        super().__init__(master)
        self.student_id = student_id
        self.proceed_callback = proceed_callback

        # Load and display background image
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(
            Image.open(asset_path),
            size=(master.winfo_screenwidth(), master.winfo_screenheight())
        )
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Centered frame above background (smaller, with more padding)
        self.center_frame = customtkinter.CTkFrame(self, width=350, height=250, corner_radius=15)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add padding inside the frame using an inner frame
        self.inner_frame = customtkinter.CTkFrame(self.center_frame, fg_color="transparent")
        self.inner_frame.pack(expand=True, fill="both", padx=30, pady=30)

        self.label = customtkinter.CTkLabel(
            self.inner_frame, text="Enter Temperature", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label.pack(pady=(0, 20))

        self.entry = customtkinter.CTkEntry(
            self.inner_frame, font=customtkinter.CTkFont(size=16), width=180
        )
        self.entry.pack(pady=10)

        self.next_button = customtkinter.CTkButton(
            self.inner_frame, text="Next", command=self.on_next, width=180
        )
        self.next_button.pack(pady=(20, 0))

    def on_next(self):
        # You can add validation here
        self.proceed_callback(self.student_id)