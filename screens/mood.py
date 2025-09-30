import customtkinter
from PIL import Image
import os
from config.supabase_client import supabase
from datetime import datetime
import json

class MoodScreen(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, on_back, student_id):
        super().__init__(master)
        self.master = master
        self.student_id = student_id
        self.selected_emotions = []  # Store selected emotions
        self.proceed_callback = proceed_callback
        self.on_back = on_back

        # Create mood frame (main frame with border) - increased height slightly for more space
        self.mood_frame = customtkinter.CTkFrame(self, corner_radius=30, border_width=3)
        self.mood_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)  # Reduced margins, increased size

        # Header label - reduced top padding
        self.header_label = customtkinter.CTkLabel(
            self.mood_frame, text="How are you feeling today?",
            font=customtkinter.CTkFont(size=28, weight="bold")
        )
        self.header_label.pack(pady=(20, 5), padx=20)  # Reduced padding

        # Emotions split into two rows
        row1 = ["Happy", "Sad", "Nothing", "Worried", "Anxious"]
        row2 = ["Confused", "Fatigue", "Dizziness", "Numb", "Irritable"]
        self.emotion_buttons = {}

        # --- Helper for image loading ---
        def get_emotion_image(emotion):
            # Map emotion to filename (lowercase, no spaces, .png)
            filename = f"{emotion.lower()}.png"
            path = os.path.join(os.path.dirname(__file__), "..", "assets", filename)
            return customtkinter.CTkImage(Image.open(path), size=(64, 64))

        # --- First row --- reduced padding
        self.emotion_frame1 = customtkinter.CTkFrame(
            self.mood_frame, fg_color="transparent"
        )
        self.emotion_frame1.pack(pady=(10, 5), padx=20)  # Reduced pady and padx
        for emotion in row1:
            btn_frame = customtkinter.CTkFrame(self.emotion_frame1, fg_color="transparent")
            btn_frame.pack(side="left", padx=10, pady=5)  # Reduced padx and pady

            img = get_emotion_image(emotion)
            btn = customtkinter.CTkButton(
                btn_frame,
                text="",  # No label on button
                image=img,
                width=70,
                height=70,
                fg_color="lightgray",
                command=lambda e=emotion: self.toggle_emotion(e)
            )
            btn.pack()
            lbl = customtkinter.CTkLabel(
                btn_frame,
                text=emotion,
                font=customtkinter.CTkFont(size=14),
                text_color="black"
            )
            lbl.pack(pady=(2, 0))  # Minimal pady for label
            self.emotion_buttons[emotion] = btn

        # --- Second row --- significantly reduced top padding to make space for buttons
        self.emotion_frame2 = customtkinter.CTkFrame(
            self.mood_frame, fg_color="transparent"
        )
        self.emotion_frame2.pack(pady=(5, 10), padx=20)  # Reduced from (80,20) to (5,10), reduced padx
        for emotion in row2:
            btn_frame = customtkinter.CTkFrame(self.emotion_frame2, fg_color="transparent")
            btn_frame.pack(side="left", padx=10, pady=5)  # Reduced padx and pady

            img = get_emotion_image(emotion)
            btn = customtkinter.CTkButton(
                btn_frame,
                text="",
                image=img,
                width=70,
                height=70,
                fg_color="lightgray",
                command=lambda e=emotion: self.toggle_emotion(e)
            )
            btn.pack()
            lbl = customtkinter.CTkLabel(
                btn_frame,
                text=emotion,
                font=customtkinter.CTkFont(size=14),
                text_color="black"
            )
            lbl.pack(pady=(2, 0))  # Minimal pady for label
            self.emotion_buttons[emotion] = btn

        # Frame for Back and Confirm buttons (no border, reduced padding)
        self.bottom_buttons_frame = customtkinter.CTkFrame(
            self.mood_frame, fg_color="transparent"
        )
        self.bottom_buttons_frame.pack(side="bottom", fill="x", pady=(10, 20), padx=20)  # Reduced pady and padx

        # Back Button - reduced width and padx for better fit
        self.back_button = customtkinter.CTkButton(
            self.bottom_buttons_frame,
            text="Back",
            font=customtkinter.CTkFont(size=18),
            width=100,  # Slightly reduced width
            height=40,
            command=self.on_back
        )
        self.back_button.pack(side="left", padx=(20, 10), pady=5)  # Reduced padx

        # Confirm Button - reduced width and padx for better fit
        self.confirm_button = customtkinter.CTkButton(
            self.bottom_buttons_frame,
            text="Confirm",
            font=customtkinter.CTkFont(size=18),
            width=100,  # Slightly reduced width
            height=40,
            command=self.on_confirm
        )
        self.confirm_button.pack(side="right", padx=(10, 20), pady=5)  # Reduced padx

    def toggle_emotion(self, emotion):
        if emotion in self.selected_emotions:
            self.selected_emotions.remove(emotion)
            self.emotion_buttons[emotion].configure(fg_color="lightgray")
        else:
            self.selected_emotions.append(emotion)
            self.emotion_buttons[emotion].configure(fg_color="#4caf50")  # Highlight selected
        print("Selected emotions:", self.selected_emotions)

    def save_mood(self):
        response = supabase.table("student_support_record").select("*").eq("student_id", self.student_id).single().execute()
        existing = response.data if response.data else {}

        record_time = existing.get("record_at", datetime.utcnow().isoformat())

        # Save all selected emotions as a JSON string in mood_level
        data = {
            "student_id": self.student_id,
            "mood_level": json.dumps(self.selected_emotions),
            "temperature": existing.get("temperature", ""),
            "blood_pressure": existing.get("blood_pressure", ""),
            "heart_rate": existing.get("heart_rate", ""),
            "record_at": record_time
        }
        print("Upserting data:", data)  # Debugging line to see the data being sent
        try:
            response = supabase.table("student_support_record").upsert(data, on_conflict=["student_id"]).execute()
            print("Supabase response:", response)  # Debugging line to see the response
            if response.data:
                print("Mood saved successfully.")
            else:
                print("Failed to save mood:", response)
        except Exception as e:
            print("Error saving mood:", e)

    def on_confirm(self):
        self.save_mood()
        self.proceed_callback()