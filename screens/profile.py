import customtkinter
from config.supabase_client import supabase
from datetime import datetime


class ProfileScreen(customtkinter.CTkFrame):
    def __init__(self, master, on_back, proceed_callback, student_data=None):
        super().__init__(master)
        self.master = master
        self.proceed_callback = proceed_callback
        self.on_back = on_back
        self.student_id = (student_data or {}).get('student_id', '')

        # Create profile frame
        self.profile_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.profile_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Instruction label
        self.instruction_label = customtkinter.CTkLabel(self.profile_frame,
            text="Complete Your Profile",
            font=customtkinter.CTkFont(size=20))
        self.instruction_label.pack(pady=20)

        # Use student_data or empty dict
        student_data = student_data or {}

        # Name (left) and Age (right)
        self.name_label = customtkinter.CTkLabel(self.profile_frame, text="Name", font=customtkinter.CTkFont(size=12))
        self.name_label.place(rely=0.10, relx=0.08, anchor="w")
        self.name_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.name_entry.place(rely=0.16, relx=0.08, anchor="w")
        name = f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}".strip()
        self.name_entry.insert(0, name)

        self.age_label = customtkinter.CTkLabel(self.profile_frame, text="Age", font=customtkinter.CTkFont(size=12))
        self.age_label.place(rely=0.10, relx=0.58, anchor="w")
        self.age_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.age_entry.place(rely=0.16, relx=0.58, anchor="w")
        self.age_entry.insert(0, str(student_data.get('age', '')))

        # Course (left) and Gender (right)
        self.course_label = customtkinter.CTkLabel(self.profile_frame, text="Course", font=customtkinter.CTkFont(size=12))
        self.course_label.place(rely=0.28, relx=0.08, anchor="w")
        self.course_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.course_entry.place(rely=0.34, relx=0.08, anchor="w")
        self.course_entry.insert(0, student_data.get('program', ''))

        self.gender_label = customtkinter.CTkLabel(self.profile_frame, text="Gender", font=customtkinter.CTkFont(size=12))
        self.gender_label.place(rely=0.28, relx=0.58, anchor="w")
        self.gender_combobox = customtkinter.CTkComboBox(self.profile_frame, width=250, values=["Male", "Female", "Other"])
        self.gender_combobox.place(rely=0.34, relx=0.58, anchor="w")
        gender_value = student_data.get('gender', '')
        if gender_value:
            self.gender_combobox.set(gender_value)
        else:
            self.gender_combobox.set("Male")

        # Year Level (left) and Weight (right)
        self.year_level_label = customtkinter.CTkLabel(self.profile_frame, text="Year Level", font=customtkinter.CTkFont(size=12))
        self.year_level_label.place(rely=0.46, relx=0.08, anchor="w")
        self.year_level_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.year_level_entry.place(rely=0.52, relx=0.08, anchor="w")
        self.year_level_entry.insert(0, student_data.get('year_level', ''))

        self.weight_label = customtkinter.CTkLabel(self.profile_frame, text="Weight (kg)", font=customtkinter.CTkFont(size=12))
        self.weight_label.place(rely=0.46, relx=0.58, anchor="w")
        self.weight_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.weight_entry.place(rely=0.52, relx=0.58, anchor="w")
        self.weight_entry.insert(0, str(student_data.get('weight', '')))

        # Email (left) and Height (right)
        self.email_label = customtkinter.CTkLabel(self.profile_frame, text="Email", font=customtkinter.CTkFont(size=12))
        self.email_label.place(rely=0.64, relx=0.08, anchor="w")
        self.email_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.email_entry.place(rely=0.70, relx=0.08, anchor="w")
        self.email_entry.insert(0, student_data.get('email', ''))

        self.height_label = customtkinter.CTkLabel(self.profile_frame, text="Height (cm)", font=customtkinter.CTkFont(size=12))
        self.height_label.place(rely=0.64, relx=0.58, anchor="w")
        self.height_entry = customtkinter.CTkEntry(self.profile_frame, font=customtkinter.CTkFont(size=12), width=250)
        self.height_entry.place(rely=0.70, relx=0.58, anchor="w")
        self.height_entry.insert(0, str(student_data.get('height', '')))

        # Back and Confirm buttons (bottom center)
        self.back_button = customtkinter.CTkButton(self.profile_frame, text="Back", command=self.on_back,
                                                     font=customtkinter.CTkFont(size=14), width=200)
        self.back_button.place(rely=0.88, relx=0.35, anchor="center")

        self.confirm_button = customtkinter.CTkButton(self.profile_frame, text="Confirm", command=self.update_profile,
                                                     font=customtkinter.CTkFont(size=14), width=200)
        self.confirm_button.place(rely=0.88, relx=0.65, anchor="center")

    def update_profile(self):
        # Split name into first and last name
        name = self.name_entry.get().strip()
        first_name, last_name = '', ''
        if ' ' in name:
            first_name, last_name = name.split(' ', 1)
        else:
            first_name = name

        data = {
            "student_id": self.student_id,
            "first_name": first_name,
            "last_name": last_name,
            "year_level": self.year_level_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "program": self.course_entry.get().strip(),
            "age": int(self.age_entry.get().strip()) if self.age_entry.get().strip().isdigit() else None,
            "height": int(self.height_entry.get().strip()) if self.height_entry.get().strip().isdigit() else None,
            "weight": int(self.weight_entry.get().strip()) if self.weight_entry.get().strip().isdigit() else None,
            "gender": self.gender_combobox.get(),
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

