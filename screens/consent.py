import customtkinter
from config.supabase_client import supabase
from datetime import datetime


consent = "Do you agree to share your recorded health and emotional status data with the University Clinic and the Office of Guidance and Counseling Services to help monitor your well-being while enrolled at USTP? consent laws for online interactions are governed by the Data Privacy Act of 2012 (RA 10173) and the Cybercrime Prevention Act of 2012 (RA 10175), which protect personal data, private communications, and prevent the spread of unauthorized intimate content."


class ConsentScreen(customtkinter.CTkFrame):
    def __init__(self, master, on_back, proceed_callback, student_id):
        super().__init__(master)
        self.master = master
        self.student_id = student_id
        self.proceed_callback = proceed_callback
        self.selected_consent = None
        self.on_back = on_back

        # Main consent frame
        self.consent_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=3)
        self.consent_frame.place(relx=0.08, rely=0.08, relwidth=0.83, relheight=0.8)

        # Use grid for precise placement
        self.consent_frame.grid_rowconfigure(0, weight=1)  # Top space
        self.consent_frame.grid_rowconfigure(1, weight=0)  # Consent label
        self.consent_frame.grid_rowconfigure(2, weight=0)  # Yes/No buttons
        self.consent_frame.grid_rowconfigure(3, weight=0)  # Message
        self.consent_frame.grid_rowconfigure(4, weight=1)  # Spacer
        self.consent_frame.grid_rowconfigure(5, weight=0)  # Bottom buttons
        self.consent_frame.grid_columnconfigure(0, weight=1)
        self.consent_frame.grid_columnconfigure(1, weight=1)

        # Consent label (top, centered, with space above)
        self.consent_label = customtkinter.CTkLabel(
            self.consent_frame, text=consent, wraplength=700,
            font=customtkinter.CTkFont(size=25, weight="bold"), justify="center"
        )
        self.consent_label.grid(row=1, column=0, columnspan=2, pady=(30, 30), sticky="n")

        # Yes/No button frame (centered, horizontal)
        self.button_frame = customtkinter.CTkFrame(self.consent_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="n")
        self.yes_button = customtkinter.CTkButton(
            self.button_frame, text="Yes", width=120, height=40,
            command=lambda: self.handle_consent(True),
            font=customtkinter.CTkFont(size=24)
        )
        self.yes_button.pack(side="left", padx=30)
        self.no_button = customtkinter.CTkButton(
            self.button_frame, text="No", width=120, height=40,
            command=lambda: self.handle_consent(False),
            font=customtkinter.CTkFont(size=24)
        )
        self.no_button.pack(side="left", padx=30)

        # Message label (centered, below Yes/No)
        self.message = customtkinter.CTkLabel(
            self.consent_frame, text="", text_color="red",
            font=customtkinter.CTkFont(size=12)
        )
        self.message.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="n")

        # Logout button (bottom left)
        self.logout_button = customtkinter.CTkButton(
            self.consent_frame, text="Logout",
            command=self.on_back,
            font=customtkinter.CTkFont(size=24), width=200, height=40
        )
        self.logout_button.grid(row=5, column=0, padx=(40, 10), pady=(10, 30), sticky="sw")

        # Confirm button (bottom right)
        self.confirm_button = customtkinter.CTkButton(
            self.consent_frame, text="Confirm",
            command=self.confirm_and_proceed,
            font=customtkinter.CTkFont(size=24), width=200, height=40
        )
        self.confirm_button.grid(row=5, column=1, padx=(10, 40), pady=(10, 30), sticky="se")

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

