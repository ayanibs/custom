import customtkinter
from config.supabase_client import supabase
from datetime import datetime

class BloodPressureScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, student_id, on_back=None):
        super().__init__(master)
        self.student_id = student_id
        self.proceed_callback = proceed_callback
        self.on_back = on_back

        # Main frame (left side, same as temperature page)
        self.center_frame = customtkinter.CTkFrame(self, width=400, height=350, corner_radius=10, border_width=3)
        self.center_frame.place(relx=0.08, rely=0.15, relwidth=0.45, relheight=0.7)

        # Inner frame for centering input
        self.inner_frame = customtkinter.CTkFrame(self.center_frame, fg_color="transparent")
        self.inner_frame.place(relx=0.5, rely=0.4, anchor="center")

        self.label = customtkinter.CTkLabel(
            self.inner_frame, text="Enter Blood Pressure", font=customtkinter.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20))

        # Subframe for input fields to group them horizontally
        self.input_frame = customtkinter.CTkFrame(self.inner_frame, fg_color="transparent")
        self.input_frame.pack(pady=10)

        # Systolic input
        self.systolic_entry = customtkinter.CTkEntry(
            self.input_frame, font=customtkinter.CTkFont(size=16), width=85, height=50, placeholder_text="Systolic"
        )
        self.systolic_entry.pack(side="left", padx=(0, 10))

        # Separator label
        self.slash_label = customtkinter.CTkLabel(
            self.input_frame, text="/", font=customtkinter.CTkFont(size=24)
        )
        self.slash_label.pack(side="left")

        # Diastolic input
        self.diastolic_entry = customtkinter.CTkEntry(
            self.input_frame, font=customtkinter.CTkFont(size=16), width=85, height=50, placeholder_text="Diastolic"
        )
        self.diastolic_entry.pack(side="left", padx=(10, 0))

        # Error label for validation messages, placed under the input frame
        self.error_label = customtkinter.CTkLabel(
            self.inner_frame, text="", font=customtkinter.CTkFont(size=12), text_color="red"
        )
        self.error_label.pack(pady=5)

        # Button frame at the bottom
        self.button_frame = customtkinter.CTkFrame(self.center_frame, fg_color="transparent")
        self.button_frame.pack(side="bottom", pady=40)

        self.back_button = customtkinter.CTkButton(
            self.button_frame, text="Back", font=customtkinter.CTkFont(size=24), width=200, height=40, command=self.on_back if self.on_back else self.default_back
        )
        self.back_button.pack(side="left", padx=20)

        self.next_button = customtkinter.CTkButton(
            self.button_frame, text="Next", font=customtkinter.CTkFont(size=24), width=200, height=40, command=self.on_next
        )
        self.next_button.pack(side="left", padx=20)

    def default_back(self):
        print("Back pressed (no handler provided)")

    def on_next(self):
        systolic_str = self.systolic_entry.get().strip()
        diastolic_str = self.diastolic_entry.get().strip()
        if not systolic_str or not diastolic_str:
            self.error_label.configure(text="Please enter both systolic and diastolic values")
            return

        try:
            systolic = float(systolic_str)
            diastolic = float(diastolic_str)
        except ValueError:
            self.error_label.configure(text="Please enter valid numbers for both fields")
            return

        if systolic < 70 or systolic > 190:
            self.error_label.configure(text="Systolic must be between 70 and 190")
            return

        if diastolic < 40 or diastolic > 120:
            self.error_label.configure(text="Diastolic must be between 40 and 120")
            return

        # Clear any previous error
        self.error_label.configure(text="")

        blood_pressure = f"{systolic_str}/{diastolic_str}"

        response = supabase.table("student_support_record").select("*").eq("student_id", self.student_id).single().execute()
        existing = response.data if response.data else {}

        record_time = existing.get("record_at", datetime.utcnow().isoformat())

        data = {
            "student_id": self.student_id,
            "temperature": existing.get("temperature", ""),
            "mood_level": existing.get("mood_level", ""),
            "blood_pressure": blood_pressure,
            "heart_rate": existing.get("heart_rate", ""),
            "record_at": record_time
        }
        try:
            supabase.table("student_support_record").upsert(data, on_conflict=["student_id"]).execute()
        except Exception as e:
            print("Error saving blood pressure:", e)
        self.proceed_callback(self.student_id)
