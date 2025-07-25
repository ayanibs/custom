
import customtkinter
from PIL import Image
import os
from supabase_client import supabase
from datetime import datetime


class VitalsignsScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, student_id):
        super().__init__(master)
        self.master = master
        self.proceed_callback = proceed_callback
        self.student_id = student_id

        # Load and create background image (same as profile)
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                              size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Create vitalsigns frame
        self.vitals_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.vitals_frame.grid(row=0, column=0, sticky="ns")

        # Header label
        self.header_label = customtkinter.CTkLabel(self.vitals_frame, text="Vital Signs", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.header_label.pack(pady=20)

        self.temp_label = customtkinter.CTkLabel(self.vitals_frame, text="Temperature", font=customtkinter.CTkFont(size=12))
        self.temp_label.pack(pady=(5, 0))
        self.temp_entry = customtkinter.CTkEntry(self.vitals_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.temp_entry.pack(pady=5)

        self.bp_label = customtkinter.CTkLabel(self.vitals_frame, text="Blood Pressure", font=customtkinter.CTkFont(size=12))
        self.bp_label.pack(pady=(5, 0))
        self.bp_entry = customtkinter.CTkEntry(self.vitals_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.bp_entry.pack(pady=5)

        self.hr_label = customtkinter.CTkLabel(self.vitals_frame, text="Heart Rate", font=customtkinter.CTkFont(size=12))
        self.hr_label.pack(pady=(5, 0))
        self.hr_entry = customtkinter.CTkEntry(self.vitals_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.hr_entry.pack(pady=5)

        # Confirm button
        self.save_button = customtkinter.CTkButton(self.vitals_frame, text="Save", command=self.save_vitalsigns,
                                                  font=customtkinter.CTkFont(size=14), width=200)
        self.save_button.pack(pady=20)

    def save_vitalsigns(self):
        # Fetch existing record for this student
        response = supabase.table("student_support_record").select("*").eq("student_id", self.student_id).execute()
        existing = response.data[0] if response.data else {}

        record_time = datetime.utcnow().isoformat()

        data = {
            "student_id": self.student_id,
            "temperature": self.temp_entry.get().strip(),
            "blood_pressure": self.bp_entry.get().strip(),
            "heart_rate": self.hr_entry.get().strip(),
            "mood_level": existing.get("mood_level", ""),  # Keep previous mood if any
            "record_at": record_time
        }
        try:
            response = supabase.table("student_support_record").upsert(data, on_conflict=["student_id"]).execute()
            if response.data:
                print("Vitalsigns saved successfully.")
                self.proceed_callback()
            else:
                print("Failed to save vitalsigns:", response)
        except Exception as e:
            print("Error saving vitalsigns:", e)