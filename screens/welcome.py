import customtkinter
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")

class WelcomeScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.proceed_callback = proceed_callback

        # Get asset paths
        current_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_path, "..", "assets")
        mood_path = os.path.join(assets_path, "mood.png")
        vital_path = os.path.join(assets_path, "vital.png")



        # Overlay frame (centered, solid color)
        self.overlay = customtkinter.CTkFrame(self, fg_color="#222222", corner_radius=10)
        self.overlay.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

        # Welcome label
        self.title_label = customtkinter.CTkLabel(
            self.overlay, text="WELCOME TO VITALSENSE",
            font=customtkinter.CTkFont(size=36, weight="bold")
        )
        self.title_label.pack(pady=(40, 30))

        # Images row
        images_frame = customtkinter.CTkFrame(self.overlay, fg_color="#222222")
        images_frame.pack(pady=(0, 30))

        # Mood image
        self.mood_img = customtkinter.CTkImage(Image.open(mood_path), size=(180, 180))
        self.mood_label = customtkinter.CTkLabel(images_frame, image=self.mood_img, text="")
        self.mood_label.pack(side="left", padx=40)

        # Vital image
        self.vital_img = customtkinter.CTkImage(Image.open(vital_path), size=(180, 180))
        self.vital_label = customtkinter.CTkLabel(images_frame, image=self.vital_img, text="")
        self.vital_label.pack(side="left", padx=40)

        # Click to continue label
        self.continue_label = customtkinter.CTkLabel(
            self.overlay, text="Click anywhere to continue",
            font=customtkinter.CTkFont(size=16)
        )
        self.continue_label.pack(pady=(20, 0))

        # Bind any click/touch to proceed
        self.bind("<Button-1>", self.on_click)
        self.overlay.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.proceed_callback:
            self.proceed_callback()