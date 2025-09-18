import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase
import subprocess
import sys

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, proceed_to_consent=None, back_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.proceed_to_consent = proceed_to_consent
        self.back_callback = back_callback

        # Asset paths
        current_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_path, "..", "assets")
        logo_path = os.path.join(assets_path, "logo.png")


        # Main frame (left side, solid color)
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=3)
        self.login_frame.place(relx=0.08, rely=0.08, relwidth=0.45, relheight=0.7,)

        # Welcome label
        self.login_label = customtkinter.CTkLabel(
            self.login_frame,
            text="Welcome to VitalSense Kiosk",
            font=customtkinter.CTkFont(size=35, weight="bold", family="Helvetica")
        )
        self.login_label.pack(pady=(40, 30))

        # Student ID entry
        self.id_entry = customtkinter.CTkEntry(
            self.login_frame, width=280, height=40, font=customtkinter.CTkFont(size=16),
            placeholder_text="Enter Student ID"
        )
        self.id_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Password entry
        self.password_entry = customtkinter.CTkEntry(
            self.login_frame, width=280, height=40, font=customtkinter.CTkFont(size=16),
            placeholder_text="Password", show="*"
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Error message label
        self.message = customtkinter.CTkLabel(
            self.login_frame, text="", text_color="red",
            font=customtkinter.CTkFont(size=12)
        )
        self.message.place(relx=0.5, rely=0.65, anchor="center")

        # Back button (smaller, under login)
        self.back_button = customtkinter.CTkButton(
            self.login_frame, text="Back", width=120, height=32,
            font=customtkinter.CTkFont(size=14),
            fg_color="#B0BEC5", hover_color="#78909C",
            command=self.on_back
        )
        self.back_button.pack(pady=(0, 20), side="bottom")

        # Login button
        self.login_button = customtkinter.CTkButton(
            self.login_frame, text="LOGIN", width=280, height=40,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            command=self.validate_login
        )
        self.login_button.pack(pady=(0, 10), side="bottom")

        # Logo and text (right side)
        self.logo_img = customtkinter.CTkImage(Image.open(logo_path), size=(250, 250))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo_img, text="")
        self.logo_label.place(relx=0.7, rely=0.21)

        self.vitalsense_label = customtkinter.CTkLabel(
            self, text="VITALSENSE",
            font=customtkinter.CTkFont(size=45, weight="bold", family="Helvetica")
        )
        self.vitalsense_label.place(relx=0.7, rely=0.65)

        # Bind focus events to show keyboard
        self.id_entry.bind("<FocusIn>", lambda event: show_keyboard())
        self.password_entry.bind("<FocusIn>", lambda event: show_keyboard())

    def validate_login(self):
        student_id = self.id_entry.get()
        password = self.password_entry.get()
        
        if not student_id or not password:
            self.message.configure(text="Please fill in all fields!")
            return

        try:
            # First, get the email associated with the student ID
            response = supabase.table('students').select('email').eq('student_id', student_id).execute()
            
            if response.data:
                email = response.data[0]['email']
                # Attempt to sign in with the retrieved email and provided password
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if auth_response.user:
                    self.message.configure(text="Login successful!", text_color="green")
                    # Proceed to consent page after login
                    if self.proceed_to_consent:
                        close_keyboard()  # <-- Close keyboard here
                        self.after(1000, lambda: self.proceed_to_consent(student_id))
                else:
                    self.message.configure(text="Invalid credentials!", text_color="red")
            else:
                self.message.configure(text="Student ID not found!", text_color="red")
                
        except Exception as e:
            self.message.configure(text=f"Login failed: {str(e)}", text_color="red")

    def on_back(self):
        if self.back_callback:
            self.back_callback()

    def exit_fullscreen(self, event=None):
        self.master.destroy()

def show_keyboard():
    if sys.platform.startswith("linux"):
        subprocess.Popen(["onboard"])
    elif sys.platform.startswith("win"):
        import os
        os.startfile("osk.exe")

def close_keyboard():
    if sys.platform.startswith("linux"):
        subprocess.Popen(["pkill", "onboard"])
    elif sys.platform.startswith("win"):
        import os
        os.system("taskkill /IM osk.exe /F")
