
import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase
from datetime import datetime

consent = "Do you agree to share your recorded health and emotional status data with the University Clinic and the Office of Guidance and Counseling Services to help monitor your well-being while enrolled at USTP?"


class ConsentScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, student_id):
        super().__init__(master)
        self.master = master
        self.student_id = student_id
        self.proceed_callback = proceed_callback
        self.selected_consent = None

        # Load and create background image (same as login page)
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                              size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Create consent frame (like login frame)
        self.consent_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.consent_frame.grid(row=0, column=0, sticky="ns")

        # Consent label
        self.consent_label = customtkinter.CTkLabel(self.consent_frame, text=consent, wraplength=600,
                                                    font=customtkinter.CTkFont(size=18, weight="bold"), justify="center")
        self.consent_label.grid(row=0, column=0, padx=30, pady=(100, 30))

        # Button frame
        self.button_frame = customtkinter.CTkFrame(self.consent_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, pady=20)

        self.yes_button = customtkinter.CTkButton(self.button_frame, text="Yes", width=100,
                                                  command=lambda: self.handle_consent(True),
                                                  font=customtkinter.CTkFont(size=16))
        self.yes_button.pack(side="left", padx=20)

        self.no_button = customtkinter.CTkButton(self.button_frame, text="No", width=100,
                                                 command=lambda: self.handle_consent(False),
                                                 font=customtkinter.CTkFont(size=16))
        self.no_button.pack(side="left", padx=20)

        # Confirm button
        self.confirm_button = customtkinter.CTkButton(self.consent_frame, text="Confirm",
                                                      command=self.confirm_and_proceed,
                                                      font=customtkinter.CTkFont(size=18), width=200)
        self.confirm_button.grid(row=2, column=0, pady=(20, 0))

        # Message label
        self.message = customtkinter.CTkLabel(self.consent_frame, text="", text_color="red",
                                              font=customtkinter.CTkFont(size=12))
        self.message.grid(row=3, column=0, pady=(10, 0))

    def handle_consent(self, consent_given):
        self.selected_consent = consent_given
        # Visual feedback for selection
        if consent_given:
            self.yes_button.configure(fg_color="#1f6aa5")
            self.no_button.configure(fg_color="#2b2b2b")
        else:
            self.no_button.configure(fg_color="#1f6aa5")
            self.yes_button.configure(fg_color="#2b2b2b")
        self.message.configure(text="")

    def confirm_and_proceed(self):
        if self.selected_consent is None:
            self.message.configure(text="Please select Yes or No before confirming.")
            return
        data = {
            "student_id": self.student_id,
            "last_update": datetime.utcnow().isoformat(),
            "consent_type": self.selected_consent
        }
        try:
            response = supabase.table("consent").upsert(data, on_conflict="student_id").execute()
            print("Supabase response:", response)
            if isinstance(response.data, list):
                self.message.configure(text="Consent recorded successfully!", text_color="green")
                # Proceed to profile page after 1 second
                self.after(1000, lambda: self.proceed_callback())
            else:
                self.message.configure(text="Failed to record consent.", text_color="red")
        except Exception as e:
            self.message.configure(text=f"Error: {e}", text_color="red")

