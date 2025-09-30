import sys
import os
import tkinter as tk  # Import base Tkinter for lower-level control
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
        self.resizable(False, False)
        self.bind("<Escape>", self.exit_fullscreen)
        self.current_frame = None
        self.input_widget = None  # Track the current input widget (e.g., Entry field)
        
        # Set up for better Linux/RPi compatibility
        if sys.platform.startswith("linux"):
            # Force Tkinter to use X11 backend if available
            os.environ['TK_SCREENSAVER'] = '0'  # Disable screensaver interference
        
        # Delay to ensure the window is fully realized before forcing fullscreen
        self.after(500, self.force_fullscreen)  # Longer delay for RPi hardware
        self.show_welcome_page()

    def force_fullscreen(self):
        # Update the window to get accurate screen dimensions
        self.update_idletasks()
        self.update()  # Additional update for stability on slow hardware
        
        # Get screen dimensions (use root attributes for accuracy)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set geometry to exact fullscreen at (0,0)
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # For Linux/RPi, use zoomed state instead of fullscreen attribute (more reliable)
        self.state('zoomed')  # Equivalent to maximized/fullscreen on many WMs
        
        # Remove all window decorations and borders
        self.overrideredirect(True)
        
        # Keep on top without topmost (avoids some focus issues)
        self.lift()
        self.attributes('-topmost', True)
        
        # Aggressive focus without global grab (global grab can fail on RPi/X11 without perms)
        self.focus_force()
        
        # Bind a periodic focus checker (every 100ms) to maintain focus on Linux quirks
        self.focus_check_id = self.after(100, self.maintain_focus)
        
        # On Linux/RPi, set window type hints for kiosk mode
        if sys.platform.startswith("linux"):
            try:
                # Hint to WM that this is a fullscreen kiosk (works with Openbox/LXDE)
                self.wm_attributes('-type', 'desktop')  # Or 'dock'/'splash' if desktop fails
                # Disable any WM controls
                self.attributes('-alpha', 1.0)  # Ensure opacity
            except tk.TclError:
                pass
            
            # Adjust geometry slightly for RPi display quirks (e.g., HDMI overscan)
            self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        print("Fullscreen mode activated. Test keyboard input now.")  # Debug print

    def maintain_focus(self):
        """Periodic check to force focus back to the app (handles Linux WM focus loss)."""
        if self.winfo_exists():  # Ensure window still exists
            self.focus_force()
            if self.input_widget and self.input_widget.winfo_exists():
                self.input_widget.focus_set()  # Focus specific input if available
            else:
                self.focus_set()
        # Reschedule
        self.focus_check_id = self.after(100, self.maintain_focus)

    def set_input_focus(self, widget):
        """Set focus to a specific input widget (e.g., Entry in login screen)."""
        self.input_widget = widget
        if widget:
            self.after(100, lambda: widget.focus_set())  # Delay for rendering

    def show_welcome_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = WelcomeScreen(self, proceed_callback=self.show_qr_page)
        self.current_frame.pack(fill="both", expand=True)
        self.input_widget = None  # No input on welcome
        self.focus_force()

    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(
            self,
            proceed_to_consent=self.show_consent_page,
            back_callback=self.show_welcome_page
        )
        self.current_frame.pack(fill="both", expand=True)
        
        # IMPORTANT: After packing, find and focus the input field (assuming LoginFrame has an Entry)
        # You may need to adjust this based on your LoginFrame structure - e.g., pass a ref or use a method
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def focus_input_in_frame(self, frame):
        """Helper to find and focus the first Entry or input widget in the frame."""
        try:
            # Search for Entry widgets (common for login)
            for child in frame.winfo_children():
                if isinstance(child, (tk.Entry, customtkinter.CTkEntry)):
                    child.focus_set()
                    self.input_widget = child
                    print("Focused input widget:", child)  # Debug
                    break
                # Recurse into subframes if needed
                elif hasattr(child, 'winfo_children'):
                    self.focus_input_in_frame(child)
        except Exception as e:
            print(f"Focus search error: {e}")

    def show_qr_page(self):
        if self.current_frame:
            if hasattr(self.current_frame, "unbind_all_widgets"):
                self.current_frame.unbind_all_widgets()
            self.current_frame.destroy()
        self.current_frame = QRFrame(self, proceed_to_login=self.show_login_page)
        self.current_frame.pack(fill="both", expand=True)
        self.input_widget = None
        self.focus_force()

    def show_consent_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ConsentScreen(self, on_back=self.show_login_page, proceed_callback=lambda: self.show_profile_page(student_id), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def show_profile_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        try:
            response = supabase.table("students").select("*").eq("student_id", student_id).execute()
            if response.data and len(response.data) > 0:
                student_data = response.data[0]
            else:
                student_data = {"student_id": student_id}
        except Exception as e:
            print(f"Error fetching student data: {e}")
            student_data = {"student_id": student_id}
        self.current_frame = ProfileScreen(
            self, on_back=lambda: self.show_consent_page(student_data.get('student_id', '')),
            proceed_callback=lambda: self.show_temperature_page(student_data.get('student_id', '')),
            student_data=student_data
        )
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def show_temperature_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TemperatureScreen(self, on_back=lambda sid=student_id: self.show_profile_page(sid), proceed_callback=lambda sid=student_id: self.show_bp_page(sid), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def show_bp_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.bp_screen import BloodPressureScreen
        self.current_frame = BloodPressureScreen(
            self,
            proceed_callback=lambda sid=student_id: self.show_hr_page(sid),
            student_id=student_id,
            on_back=lambda sid=student_id: self.show_temperature_page(sid)
        )
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def show_hr_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.hr_screen import HeartRateScreen
        self.current_frame = HeartRateScreen(
            self,
            proceed_callback=lambda sid=student_id: self.show_mood_page(sid),
            student_id=student_id,
            on_back=lambda sid=student_id: self.show_bp_page(sid)
        )
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def show_mood_page(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.mood import MoodScreen
        self.current_frame = MoodScreen(self, proceed_callback=lambda: self.show_logout_page(student_id), on_back=lambda: self.show_hr_page(student_id), student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def show_logout_page(self, student_id=None):
        if self.current_frame:
            self.current_frame.destroy()
        from screens.logout import LogoutScreen
        self.current_frame = LogoutScreen(self, logout_callback=self.show_login_page, student_id=student_id)
        self.current_frame.pack(fill="both", expand=True)
        self.after(200, lambda: self.focus_input_in_frame(self.current_frame))
        self.focus_force()

    def exit_fullscreen(self, event=None):
        # Stop the focus checker
        if hasattr(self, 'focus_check_id'):
            self.after_cancel(self.focus_check_id)
        self.attributes('-topmost', False)
        self.overrideredirect(False)
        self.state('normal')  # Restore normal state
        self.destroy()

