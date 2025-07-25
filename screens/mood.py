
import customtkinter
from PIL import Image
import os
from supabase_client import supabase
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

        # Load and create background image (same as other screens)
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(current_path, "..", "assets", "background.png")
        self.bg_image = customtkinter.CTkImage(Image.open(asset_path),
                                              size=(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Create mood frame
        self.mood_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.mood_frame.grid(row=0, column=0, sticky="ns")

        # Header label
        self.header_label = customtkinter.CTkLabel(self.mood_frame, text="How are you feeling today?", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.header_label.pack(pady=30)

        # Emotions
        emotions = ["Happy", "Nothing", "Sad", "Worried", "Anxious"]
        self.emotion_buttons = {}
        self.emotion_frame = customtkinter.CTkFrame(self.mood_frame)
        self.emotion_frame.pack(pady=40)
        for emotion in emotions:
            btn = customtkinter.CTkButton(self.emotion_frame,
                                          text=emotion,
                                          font=customtkinter.CTkFont(size=16),
                                          width=120,
                                          height=40,
                                          fg_color="lightgray",
                                          text_color="black",
                                          command=lambda e=emotion: self.toggle_emotion(e))
            btn.pack(side="left", padx=20, pady=10)
            self.emotion_buttons[emotion] = btn

        # Frame for Back and Confirm buttons
        self.bottom_buttons_frame = customtkinter.CTkFrame(self.mood_frame)
        self.bottom_buttons_frame.pack(side="bottom", fill="x", pady=50)

        # Back Button
        self.back_button = customtkinter.CTkButton(self.bottom_buttons_frame,
                                                   text="Back",
                                                   font=customtkinter.CTkFont(size=18),
                                                   fg_color="black",
                                                   text_color="white",
                                                   width=120,
                                                   height=40,
                                                   command=self.on_back)
        self.back_button.pack(side="left", padx=(50, 0))

        # Confirm Button
        self.confirm_button = customtkinter.CTkButton(self.bottom_buttons_frame,
                                                      text="Confirm",
                                                      font=customtkinter.CTkFont(size=18),
                                                      fg_color="black",
                                                      text_color="white",
                                                      width=120,
                                                      height=40,
                                                      command=self.on_confirm)
        self.confirm_button.pack(side="right", padx=(0, 50))

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
