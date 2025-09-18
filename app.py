import customtkinter
from screens.welcome import WelcomeScreen
from screens.loginpage import LoginFrame
from screens.qr import QRFrame
from screens.consent import ConsentScreen
from screens.profile import ProfileScreen
from screens.temperature import TemperatureScreen
from config.supabase_client import supabase


class KioskApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("VitalSense Kiosk")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.exit_fullscreen)  # Allow exit fullscreen with Escape key
        self.resizable(False, False)
        self.current_frame = None
        self.show_welcome_page()  # Show welcome screen first


    def show_welcome_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = WelcomeScreen(self, proceed_callback=self.show_qr_page)
        self.current_frame.pack(fill="both", expand=True)

    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(
            self,
            proceed_to_consent=self.show_consent_page,
            back_callback=self.show_welcome_page  # <-- Add this
        )
        self.current_frame.pack(fill="both", expand=True)


    def show_qr_page(self):
        if self.current_frame:
            if hasattr(self.current_frame, "unbind_all_widgets"):
                self.current_frame.unbind_all_widgets()
            self.current_frame.destroy()
        self.current_frame = QRFrame(self, proceed_to_login=self.show_login_page)
        self.current_frame.pack(fill="both", expand=True)


    def show_consent_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        # Pass a callback that takes student_id and shows the profile page
        self.current_frame = ConsentScreen(self, on_back=self.show_login_page, proceed_callback=lambda: self.show_profile_page(student_id), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def show_profile_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        # Fetch student data from Supabase
        try:
            response = supabase.table("students").select("*").eq("student_id", student_id).execute()
            if response.data and len(response.data) > 0:
                student_data = response.data[0]
            else:
                student_data = {"student_id": student_id}
        except Exception as e:
            print(f"Error fetching student data: {e}")
            student_data = {"student_id": student_id}
        # Pass a callback that includes the student_id for vitalsigns
        self.current_frame = ProfileScreen(
            self, on_back=lambda: self.show_consent_page(student_data.get('student_id', '')),
            proceed_callback=lambda: self.show_temperature_page(student_data.get('student_id', '')),
            student_data=student_data
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_temperature_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TemperatureScreen(self, on_back=lambda sid=student_id: self.show_profile_page(sid), proceed_callback=lambda sid=student_id: self.show_bp_page(sid), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def show_bp_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.bp_screen import BloodPressureScreen
        self.current_frame = BloodPressureScreen(
            self,
            proceed_callback=lambda sid=student_id: self.show_hr_page(sid),
            student_id=student_id,
            on_back=lambda sid=student_id: self.show_temperature_page(sid)  # <-- Add this
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_hr_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.hr_screen import HeartRateScreen
        self.current_frame = HeartRateScreen(
            self,
            proceed_callback=lambda sid=student_id: self.show_mood_page(sid),
            student_id=student_id,
            on_back=lambda sid=student_id: self.show_bp_page(sid)  # <-- Add this
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_mood_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.mood import MoodScreen
        self.current_frame = MoodScreen(self, proceed_callback=lambda: self.show_logout_page(student_id), on_back=lambda: self.show_hr_page(student_id), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def show_logout_page(self, student_id=None):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.logout import LogoutScreen
        self.current_frame = LogoutScreen(self, logout_callback=self.show_login_page, student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def exit_fullscreen(self, event=None):
        self.destroy()