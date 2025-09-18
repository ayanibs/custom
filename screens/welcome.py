import customtkinter
from PIL import Image
import os


class WelcomeScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.proceed_callback = proceed_callback
        self.bind_all_widgets()

        # Get asset paths
        current_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_path, "..", "assets")
        mood_path = os.path.join(assets_path, "mood.png")
        vital_path = os.path.join(assets_path, "vital.png")

        # Overlay frame (centered, solid color)
        self.overlay = customtkinter.CTkFrame(self, corner_radius=10, border_width=3)
        self.overlay.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Add internal padding to overlay frame
        self.overlay.grid_rowconfigure(0, weight=1)
        self.overlay.grid_columnconfigure(0, weight=1)

        # Welcome label
        self.title_label = customtkinter.CTkLabel(
            self.overlay, text="WELCOME TO VITALSENSE",
            font=customtkinter.CTkFont(size=45, weight="bold", family="Helvetica")
        )
        self.title_label.pack(pady=(40, 10), padx=20)  # Add horizontal padding

        # Images row (centered vertically with expand)
        images_frame = customtkinter.CTkFrame(self.overlay, fg_color="transparent")
        images_frame.pack(expand=False, fill="x", pady=(0, 0), padx=20)  # Add horizontal padding

        # Mood image
        self.mood_img = customtkinter.CTkImage(Image.open(mood_path), size=(400, 400))
        self.mood_label = customtkinter.CTkLabel(images_frame, image=self.mood_img, text="")
        self.mood_label.grid(row=1, column=0, padx=(8, 8), pady=0, sticky="ew")  # Add padding

        # Vital image
        self.vital_img = customtkinter.CTkImage(Image.open(vital_path), size=(400, 400))
        self.vital_label = customtkinter.CTkLabel(images_frame, image=self.vital_img, text="")
        self.vital_label.grid(row=1, column=1, padx=(8, 8), pady=0, sticky="w")  # Add padding

        # Make columns expand equally
        images_frame.grid_columnconfigure(0, weight=1)
        images_frame.grid_columnconfigure(1, weight=1)
        images_frame.grid_rowconfigure(0, weight=1)

        # Click to continue label at the bottom
        self.continue_label = customtkinter.CTkLabel(
            self.overlay, text="Click anywhere to continue",
            font=customtkinter.CTkFont(size=16)
        )
        self.continue_label.pack(pady=(0, 40), padx=20, side="bottom")  # Add horizontal padding

    def bind_all_widgets(self):
        root = self.winfo_toplevel()
        root.bind("<Button-1>", self.on_click)

    def unbind_all_widgets(self):
        root = self.winfo_toplevel()
        root.unbind("<Button-1>")

    def on_click(self, event):
        if self.proceed_callback:
            self.proceed_callback()