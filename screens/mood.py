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

        # Create mood frame (main frame with border)
        self.mood_frame = customtkinter.CTkFrame(self, corner_radius=30, border_width=3)
        self.mood_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Header label
        self.header_label = customtkinter.CTkLabel(
            self.mood_frame, text="How are you feeling today?",
            font=customtkinter.CTkFont(size=28, weight="bold")
        )
        self.header_label.pack(pady=(30, 10), padx=30)  # Add horizontal padding

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

        # --- First row ---
        self.emotion_frame1 = customtkinter.CTkFrame(
            self.mood_frame, fg_color="transparent"
        )
        self.emotion_frame1.pack(pady=(20, 10), padx=30)  # Reduced pady
        for emotion in row1:
            btn_frame = customtkinter.CTkFrame(self.emotion_frame1, fg_color="transparent")
            btn_frame.pack(side="left", padx=18, pady=10)

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
            lbl.pack(pady=(5, 0))
            self.emotion_buttons[emotion] = btn

        # --- Second row ---
        self.emotion_frame2 = customtkinter.CTkFrame(
            self.mood_frame, fg_color="transparent"
        )
        self.emotion_frame2.pack(pady=(80, 20), padx=30)
        for emotion in row2:
            btn_frame = customtkinter.CTkFrame(self.emotion_frame2, fg_color="transparent")
            btn_frame.pack(side="left", padx=18, pady=10)

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
            lbl.pack(pady=(5, 0))
            self.emotion_buttons[emotion] = btn

        # Frame for Back and Confirm buttons (no border, add padding)
        self.bottom_buttons_frame = customtkinter.CTkFrame(
            self.mood_frame, fg_color="transparent"
        )
        self.bottom_buttons_frame.pack(side="bottom", fill="x", pady=(20, 30), padx=30)  # Add horizontal padding

        # Back Button
        self.back_button = customtkinter.CTkButton(
            self.bottom_buttons_frame,
            text="Back",
            font=customtkinter.CTkFont(size=18),
            width=120,
            height=40,
            command=self.on_back
        )
        self.back_button.pack(side="left", padx=(50, 0), pady=10)

        # Confirm Button
        self.confirm_button = customtkinter.CTkButton(
            self.bottom_buttons_frame,
            text="Confirm",
            font=customtkinter.CTkFont(size=18),
            width=120,
            height=40,
            command=self.on_confirm
        )
        self.confirm_button.pack(side="right", padx=(0, 50), pady=10)

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
