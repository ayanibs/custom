import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase
from datetime import datetime

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
        temperature = self.entry.get()
        if not temperature:
            # Optionally show an error message
            return

        # Fetch existing record
        response = supabase.table("student_support_record").select("*").eq("student_id", self.student_id).single().execute()
        existing = response.data if response.data else {}

        record_time = existing.get("record_at", datetime.utcnow().isoformat())

        data = {
            "student_id": self.student_id,
            "temperature": temperature,
            "mood_level": existing.get("mood_level", ""),
            "blood_pressure": existing.get("blood_pressure", ""),
            "heart_rate": existing.get("heart_rate", ""),
            "record_at": record_time
        }
        try:
            supabase.table("student_support_record").upsert(data, on_conflict=["student_id"]).execute()
        except Exception as e:
            print("Error saving temperature:", e)
        self.proceed_callback(self.student_id)