import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase

customtkinter.set_appearance_mode("dark")

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, proceed_to_consent=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.proceed_to_consent = proceed_to_consent

        # Asset paths
        current_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_path, "..", "assets")
        bg_path = os.path.join(assets_path, "background.png")
        logo_path = os.path.join(assets_path, "logo.png")

        # Background image
        self.bg_image = customtkinter.CTkImage(
            Image.open(bg_path),
            size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight())
        )
        self.bg_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Main frame (left side, solid color)
        self.login_frame = customtkinter.CTkFrame(self, fg_color="#222222", corner_radius=10)
        self.login_frame.place(relx=0.08, rely=0.12, relwidth=0.45, relheight=0.65)

        # Welcome label
        self.login_label = customtkinter.CTkLabel(
            self.login_frame,
            text="Welcome to VitalSense Kiosk",
            font=customtkinter.CTkFont(size=28, weight="bold")
        )
        self.login_label.pack(pady=(40, 30))

        # Student ID entry
        self.id_entry = customtkinter.CTkEntry(
            self.login_frame, width=280, height=40, font=customtkinter.CTkFont(size=16),
            placeholder_text="Enter Student ID"
        )
        self.id_entry.pack(pady=(0, 20))

        # Password entry
        self.password_entry = customtkinter.CTkEntry(
            self.login_frame, width=280, height=40, font=customtkinter.CTkFont(size=16),
            placeholder_text="Password", show="*"
        )
        self.password_entry.pack(pady=(0, 20))

        # Error message label
        self.message = customtkinter.CTkLabel(
            self.login_frame, text="", text_color="red",
            font=customtkinter.CTkFont(size=12)
        )
        self.message.pack(pady=(0, 10))

        # Login button
        self.login_button = customtkinter.CTkButton(
            self.login_frame, text="LOGIN", width=280, height=40,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            fg_color="#2196F3", hover_color="#1976D2",
            command=self.validate_login
        )
        self.login_button.pack(pady=(10, 10))

        # Logo and text (right side)
        self.logo_img = customtkinter.CTkImage(Image.open(logo_path), size=(200, 200))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo_img, text="")
        self.logo_label.place(relx=0.62, rely=0.18)

        self.vitalsense_label = customtkinter.CTkLabel(
            self, text="VITALSENSE",
            font=customtkinter.CTkFont(size=36, weight="bold")
        )
        self.vitalsense_label.place(relx=0.62, rely=0.48)

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
                        self.after(1000, lambda: self.proceed_to_consent(student_id))
                else:
                    self.message.configure(text="Invalid credentials!", text_color="red")
            else:
                self.message.configure(text="Student ID not found!", text_color="red")
                
        except Exception as e:
            self.message.configure(text=f"Login failed: {str(e)}", text_color="red")

    def exit_fullscreen(self, event=None):
        self.master.destroy()
