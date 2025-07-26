import customtkinter
from PIL import Image
import os
from supabase_client import supabase

customtkinter.set_appearance_mode("dark")


# LoginFrame is now a frame, not a root window
class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, proceed_to_consent=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.proceed_to_consent = proceed_to_consent

        # load and create background image
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                             size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.login_frame.grid(row=0, column=0, padx=40, pady=40)

        
        image_path = os.path.join(current_path, "..", "assets", "logo.png")

        self.image = customtkinter.CTkImage(Image.open(image_path), size=(170, 170))
        self.image_label = customtkinter.CTkLabel(self.login_frame, image=self.image, text="")
        self.image_label.grid(row=1, column=0, padx=30, pady=(10, 15)) 

        # Welcome label
        self.login_label = customtkinter.CTkLabel(self.login_frame, 
                                                text="Welcome to VitalSense Kiosk",
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=2, column=0, padx=30, pady=(10, 15))


        # Student ID and Password entry fields
        self.id_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Enter Student ID")
        self.id_entry.grid(row=4, column=0, padx=30, pady=(0, 15))

        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Password",show="*")
        self.password_entry.grid(row=5, column=0, padx=30, pady=(15, 15))


        # Error message label
        self.message = customtkinter.CTkLabel(self.login_frame, text="",
                                            text_color="red",
                                            font=customtkinter.CTkFont(size=12))
        self.message.grid(row=6, column=0, padx=30, pady=(0, 15))

        # Login button
        self.login_button = customtkinter.CTkButton(self.login_frame, 
                                                  text="Login", 
                                                  command=self.validate_login,
                                                  width=200)
        self.login_button.grid(row=6, column=0, padx=30, pady=(50, 15))


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
