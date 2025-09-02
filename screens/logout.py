
import customtkinter
from config.supabase_client import supabase

class LogoutScreen(customtkinter.CTkFrame):
    def __init__(self, master, logout_callback, student_id=None):
        super().__init__(master)
        self.master = master
        self.student_id = student_id

        # Create logout frame
        self.logout_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.logout_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Thank you message
        self.thank_label = customtkinter.CTkLabel(self.logout_frame,
            text="Thank you for using VITALSENSE!",
            font=customtkinter.CTkFont(size=45, weight="bold", family="Helvetica"),
            text_color="black"
        )
        self.thank_label.pack(pady=(200, 20))

        # Press anywhere message
        self.press_label = customtkinter.CTkLabel(self.logout_frame,
            text="Press anywhere to continue",
            font=customtkinter.CTkFont(size=18),
            text_color="black"
        )
        self.press_label.pack(pady=10)

        # Log out the student from Supabase Auth if logged in
        try:
            supabase.auth.sign_out()
        except Exception as e:
            print("Logout error:", e)

        # Bind any mouse click event on this frame to the logout_callback
        self.bind("<Button-1>", lambda event: logout_callback())
        for widget in self.winfo_children():
            widget.bind("<Button-1>", lambda event: logout_callback())