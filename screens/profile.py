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

        # Centered profile frame
        self.profile_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=3)
        self.profile_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Font sizes
        label_font = customtkinter.CTkFont(size=17, weight="bold")
        entry_font = customtkinter.CTkFont(size=16)
        entry_width = 320
        entry_height = 50

        # Instruction label (centered at top)
        self.instruction_label = customtkinter.CTkLabel(
            self.profile_frame, text="Complete Your Profile", font=customtkinter.CTkFont(size=28, weight="bold")
        )
        self.instruction_label.place(relx=0.5, rely=0.07, anchor="center")

        student_data = student_data or {}

        # Vertical positions for each row
        row_positions = [0.23, 0.38, 0.53, 0.68]

        # Name
        self.name_label = customtkinter.CTkLabel(self.profile_frame, text="Name", font=label_font)
        self.name_label.place(relx=0.10, rely=row_positions[0], anchor="e")
        self.name_entry = customtkinter.CTkEntry(self.profile_frame, font=entry_font, width=entry_width, height=entry_height, placeholder_text="Ex. Juan Dela Cruz")
        self.name_entry.place(relx=0.13, rely=row_positions[0], anchor="w")
        name = f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}".strip()
        self.name_entry.insert(0, name)

        # Age
        self.age_label = customtkinter.CTkLabel(self.profile_frame, text="Age", font=label_font)
        self.age_label.place(relx=0.60, rely=row_positions[0], anchor="e")
        self.age_entry = customtkinter.CTkEntry(self.profile_frame, font=entry_font, width=entry_width, height=entry_height, placeholder_text="Ex. 20")
        self.age_entry.place(relx=0.63, rely=row_positions[0], anchor="w")
        self.age_entry.insert(0, str(student_data.get('age', '')))

        # Course
        self.course_label = customtkinter.CTkLabel(self.profile_frame, text="Course", font=label_font)
        self.course_label.place(relx=0.10, rely=row_positions[1], anchor="e")
        course_choices = [
            "Bachelor in Technical-Vocational Teacher Education",
            "Bachelor in Technology and Livelihood Education",
            "Bachelor of Science in Applied Mathematics",
            "Bachelor of Science in Applied Physics",
            "Bachelor of Science in Architecture",
            "Bachelor of Science in Autotronics",
            "Bachelor of Science in Chemistry",
            "Bachelor of Science in Civil Engineering",
            "Bachelor of Science in Computer Engineering",
            "Bachelor of Science in Computer Science",
            "Bachelor of Science in Data Science",
            "Bachelor of Science in Electrical Engineering",
            "Bachelor of Science in Electro-Mechanical Technology",
            "Bachelor of Science in Electronics Engineering",
            "Bachelor of Science in Electronics Technology",
            "Bachelor of Science in Energy Systems and Management",
            "Bachelor of Science in Environmental Science",
            "Bachelor of Science in Food Technology",
            "Bachelor of Science in Geodetic Engineering",
            "Bachelor of Science in Information Technology",
            "Bachelor of Science in Manufacturing Engineering Technology",
            "Bachelor of Science in Mechanical Engineering",
            "Bachelor of Science in Technology Communication Management",
            "Bachelor of Technology, Operations, and Management",
            "Bachelor of Secondary Education"
        ]
        self.course_combobox = customtkinter.CTkComboBox(self.profile_frame, width=entry_width, height=entry_height, font=entry_font, values=course_choices)
        self.course_combobox.place(relx=0.13, rely=row_positions[1], anchor="w")
        course_value = student_data.get('program', '')
        if course_value and course_value in course_choices:
            self.course_combobox.set(course_value)
        else:
            self.course_combobox.set(course_choices[0])

        # Gender
        self.gender_label = customtkinter.CTkLabel(self.profile_frame, text="Gender", font=label_font)
        self.gender_label.place(relx=0.60, rely=row_positions[1], anchor="e")
        self.gender_combobox = customtkinter.CTkComboBox(self.profile_frame, width=entry_width, height=entry_height, font=entry_font, values=["Male", "Female", "Other"])
        self.gender_combobox.place(relx=0.63, rely=row_positions[1], anchor="w")
        gender_value = student_data.get('gender', '')
        if gender_value:
            self.gender_combobox.set(gender_value)
        else:
            self.gender_combobox.set("Male")

        # Year Level
        self.year_level_label = customtkinter.CTkLabel(self.profile_frame, text="Year Level", font=label_font)
        self.year_level_label.place(relx=0.10, rely=row_positions[2], anchor="e")
        year_choices = ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"]
        self.year_level_entry = customtkinter.CTkComboBox(self.profile_frame, width=entry_width, height=entry_height, font=entry_font, values=year_choices)
        self.year_level_entry.place(relx=0.13, rely=row_positions[2], anchor="w")
        year_level_value = student_data.get('year_level', '')
        if year_level_value and year_level_value in year_choices:
            self.year_level_entry.set(year_level_value)
        else:
            self.year_level_entry.set(year_choices[0])

        # Weight
        self.weight_label = customtkinter.CTkLabel(self.profile_frame, text="Weight (kg)", font=label_font)
        self.weight_label.place(relx=0.60, rely=row_positions[2], anchor="e")
        self.weight_entry = customtkinter.CTkEntry(self.profile_frame, font=entry_font, width=entry_width, height=entry_height, placeholder_text="Ex. 70(kg)")
        self.weight_entry.place(relx=0.63, rely=row_positions[2], anchor="w")
        self.weight_entry.insert(0, str(student_data.get('weight', '')))

        # Email
        self.email_label = customtkinter.CTkLabel(self.profile_frame, text="Email", font=label_font)
        self.email_label.place(relx=0.10, rely=row_positions[3], anchor="e")
        self.email_entry = customtkinter.CTkEntry(self.profile_frame, font=entry_font, width=entry_width, height=entry_height)
        self.email_entry.place(relx=0.13, rely=row_positions[3], anchor="w")
        self.email_entry.insert(0, student_data.get('email', ''))

        # Height
        self.height_label = customtkinter.CTkLabel(self.profile_frame, text="Height (cm)", font=label_font)
        self.height_label.place(relx=0.60, rely=row_positions[3], anchor="e")
        self.height_entry = customtkinter.CTkEntry(self.profile_frame, font=entry_font, width=entry_width, height=entry_height, placeholder_text="Ex. 170(cm)")
        self.height_entry.place(relx=0.63, rely=row_positions[3], anchor="w")
        self.height_entry.insert(0, str(student_data.get('height', '')))

        # Back and Confirm buttons (centered at bottom)
        self.back_button = customtkinter.CTkButton(self.profile_frame, text="Back", command=self.on_back,
                                                     font=customtkinter.CTkFont(size=24), width=200, height=40)
        self.back_button.place(relx=0.38, rely=0.88, anchor="center")

        self.confirm_button = customtkinter.CTkButton(self.profile_frame, text="Confirm", command=self.update_profile,
                                                     font=customtkinter.CTkFont(size=24), width=200, height=40)
        self.confirm_button.place(relx=0.60, rely=0.88, anchor="center")

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
            "program": self.course_combobox.get(),
            "age": int(self.age_entry.get().strip()) if self.age_entry.get().strip().isdigit() else "",
            "height": int(self.height_entry.get().strip()) if self.height_entry.get().strip().isdigit() else "",
            "weight": int(self.weight_entry.get().strip()) if self.weight_entry.get().strip().isdigit() else "",
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

