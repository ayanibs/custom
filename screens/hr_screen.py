import customtkinter
from config.supabase_client import supabase
from datetime import datetime

class HeartRateScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, student_id, on_back=None):
        super().__init__(master)
        self.student_id = student_id
        self.proceed_callback = proceed_callback
        self.on_back = on_back

        # Main frame (left side, same as temperature page)
        self.center_frame = customtkinter.CTkFrame(self, width=400, height=350, corner_radius=10, border_width=3)
        self.center_frame.place(relx=0.08, rely=0.08, relwidth=0.45, relheight=0.7)

        # Inner frame for centering input
        self.inner_frame = customtkinter.CTkFrame(self.center_frame, fg_color="transparent")
        self.inner_frame.place(relx=0.5, rely=0.4, anchor="center")

        self.label = customtkinter.CTkLabel(
            self.inner_frame, text="Enter Heart Rate", font=customtkinter.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20))

        self.entry = customtkinter.CTkEntry(
            self.inner_frame, font=customtkinter.CTkFont(size=16), width=180, height=50, placeholder_text="Ex. 75"
        )
        self.entry.pack(pady=10)

        # Error label for validation messages, placed under the input field
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
        heart_rate_str = self.entry.get().strip()
        if not heart_rate_str:
            self.error_label.configure(text="Please enter heart rate")
            return

        try:
            heart_rate = float(heart_rate_str)
        except ValueError:
            self.error_label.configure(text="Please enter a valid number")
            return

        if heart_rate < 75 or heart_rate > 170:
            self.error_label.configure(text="Heart rate must be between 75 and 170")
            return

        # Clear any previous error
        self.error_label.configure(text="")

        response = supabase.table("student_support_record").select("*").eq("student_id", self.student_id).single().execute()
        existing = response.data if response.data else {}

        record_time = existing.get("record_at", datetime.utcnow().isoformat())

        data = {
            "student_id": self.student_id,
            "temperature": existing.get("temperature", ""),
            "mood_level": existing.get("mood_level", ""),
            "blood_pressure": existing.get("blood_pressure", ""),
            "heart_rate": heart_rate_str,  # Store as string to preserve original input format
            "record_at": record_time
        }
        try:
            supabase.table("student_support_record").upsert(data, on_conflict=["student_id"]).execute()
        except Exception as e:
            print("Error saving heart rate:", e)
        self.proceed_callback(self.student_id)
