import customtkinter
from PIL import Image
import os


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
        self.overlay.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Welcome label
        self.title_label = customtkinter.CTkLabel(
            self.overlay, text="WELCOME TO VITALSENSE",
            font=customtkinter.CTkFont(size=36, weight="bold")
        )
        self.title_label.pack(pady=(40, 10))  # Remove bottom padding

        # Images row (centered vertically with expand)
        images_frame = customtkinter.CTkFrame(self.overlay, fg_color="#222222")
        images_frame.pack(expand=True, fill="both", pady=(0, 0))

        # Mood image
        self.mood_img = customtkinter.CTkImage(Image.open(mood_path), size=(700, 400))
        self.mood_label = customtkinter.CTkLabel(images_frame, image=self.mood_img, text="")
        self.mood_label.grid(row=0, column=0, padx=(0, 8), pady=0, sticky="e")  # Small space

        # Vital image
        self.vital_img = customtkinter.CTkImage(Image.open(vital_path), size=(700, 400))
        self.vital_label = customtkinter.CTkLabel(images_frame, image=self.vital_img, text="")
        self.vital_label.grid(row=0, column=1, padx=(8, 0), pady=0, sticky="w")  # Small space

        # Make columns expand equally
        images_frame.grid_columnconfigure(0, weight=1)
        images_frame.grid_columnconfigure(1, weight=1)
        images_frame.grid_rowconfigure(0, weight=1)

        # Click to continue label at the bottom
        self.continue_label = customtkinter.CTkLabel(
            self.overlay, text="Click anywhere to continue",
            font=customtkinter.CTkFont(size=16)
        )
        self.continue_label.pack(pady=(0, 40), side="bottom")  # Add bottom padding

        # Bind click event to all widgets recursively
        self.bind_all_widgets(self)

    def bind_all_widgets(self, widget):
        widget.bind("<Button-1>", self.on_click)
        for child in widget.winfo_children():
            self.bind_all_widgets(child)

    def on_click(self, event):
        if self.proceed_callback:
            self.proceed_callback()