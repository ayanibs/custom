import customtkinter
from screens.loginpage import LoginFrame
from screens.qr import QRFrame
from screens.consent import ConsentScreen
from screens.profile import ProfileScreen
from screens.vitalsigns import VitalsignsScreen
from supabase_client import supabase


class KioskApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("VitalSense Kiosk")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.exit_fullscreen)  # Allow exit fullscreen with Escape key
        self.resizable(False, False)
        self.current_frame = None
        self.show_qr_page()


    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, proceed_to_consent=self.show_consent_page)
        self.current_frame.pack(fill="both", expand=True)


    def show_qr_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = QRFrame(self)
        self.current_frame.pack(fill="both", expand=True)


    def show_consent_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        # Pass a callback that takes student_id and shows the profile page
        self.current_frame = ConsentScreen(self, proceed_callback=lambda: self.show_profile_page(student_id), student_id=student_id)
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
        self.current_frame = ProfileScreen(self, proceed_callback=lambda: self.show_next_page(student_data.get('student_id', '')), student_data=student_data)
        self.current_frame.pack(fill="both", expand=True)

    def show_next_page(self, student_id):
        # Proceed to vitalsigns page after profile
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = VitalsignsScreen(self, proceed_callback=lambda: self.show_mood_page(student_id), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def show_mood_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.mood import MoodScreen
        self.current_frame = MoodScreen(self, proceed_callback=lambda: self.show_logout_page(student_id), on_back=lambda: self.show_next_page(student_id), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def show_logout_page(self, student_id=None):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.logout import LogoutScreen
        self.current_frame = LogoutScreen(self, logout_callback=self.show_login_page, student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)

    def exit_fullscreen(self, event=None):
        self.destroy()