import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase
from datetime import datetime


class ProfileScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, student_data=None):
        super().__init__(master)
        self.master = master
        self.proceed_callback = proceed_callback
        self.student_id = (student_data or {}).get('student_id', '')

        # Load and create background image (same as login/consent)
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                              size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Create profile frame
        self.profile_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.profile_frame.grid(row=0, column=0, sticky="ns")

        # Instruction label
        self.instruction_label = customtkinter.CTkLabel(self.profile_frame,
            text="*Is this information correct? If not, please tap the boxes to update it.",
            font=customtkinter.CTkFont(size=14))
        self.instruction_label.pack(pady=20)

        # Use student_data or empty dict
        student_data = student_data or {}

        self.id_number_label = customtkinter.CTkLabel(self.profile_frame, text="ID Number", font=customtkinter.CTkFont(size=12))
        self.id_number_label.pack(pady=(5, 0))
        self.id_number_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.id_number_entry.pack(pady=5)
        self.id_number_entry.insert(0, student_data.get('student_id', ''))

        self.course_label = customtkinter.CTkLabel(self.profile_frame, text="Course", font=customtkinter.CTkFont(size=12))
        self.course_label.pack(pady=(5, 0))
        self.course_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.course_entry.pack(pady=5)
        self.course_entry.insert(0, student_data.get('program', ''))

        self.name_label = customtkinter.CTkLabel(self.profile_frame, text="Name", font=customtkinter.CTkFont(size=12))
        self.name_label.pack(pady=(5, 0))
        self.name_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.name_entry.pack(pady=5)
        # Combine first and last name
        name = f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}".strip()
        self.name_entry.insert(0, name)

        self.year_level_label = customtkinter.CTkLabel(self.profile_frame, text="Year Level", font=customtkinter.CTkFont(size=12))
        self.year_level_label.pack(pady=(5, 0))
        self.year_level_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.year_level_entry.pack(pady=5)
        self.year_level_entry.insert(0, student_data.get('year_level', ''))

        self.email_label = customtkinter.CTkLabel(self.profile_frame, text="Email", font=customtkinter.CTkFont(size=12))
        self.email_label.pack(pady=(5, 0))
        self.email_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, student_data.get('email', ''))

        self.contact_label = customtkinter.CTkLabel(self.profile_frame, text="Contact Number", font=customtkinter.CTkFont(size=12))
        self.contact_label.pack(pady=(5, 0))
        self.contact_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=300)
        self.contact_entry.pack(pady=5)
        self.contact_entry.insert(0, student_data.get('contact_number', ''))

        self.confirm_button = customtkinter.CTkButton(self.profile_frame, text="Confirm", command=self.update_profile,
                                                     font=customtkinter.CTkFont(size=14), width=200)
        self.confirm_button.pack(pady=20)

    def update_profile(self):
        # Split name into first and last name
        name = self.name_entry.get().strip()
        first_name, last_name = '', ''
        if ' ' in name:
            first_name, last_name = name.split(' ', 1)
        else:
            first_name = name

        data = {
            "student_id": self.id_number_entry.get().strip(),
            "first_name": first_name,
            "last_name": last_name,
            "year_level": self.year_level_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "program": self.course_entry.get().strip(),
            "contact_number": self.contact_entry.get().strip(),
            "last_update": datetime.utcnow().isoformat()
        }

        try:
            # Update the student record in Supabase
            response = supabase.table("students").update(data).eq("student_id", self.student_id).execute()
            if response.data:
                print("Profile updated successfully.")
                self.proceed_callback()
            else:
                print("Failed to update profile:", response)
        except Exception as e:
            print("Error updating profile:", e)


