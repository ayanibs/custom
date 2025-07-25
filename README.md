kiosk_app/
│
├── main.py
├── screens/
│   ├── __init__.py
│   ├── login_screen.py
│   ├── Signup_screen.py
|   ├── Consent_screen.py
|   ├── Profile.screen.py
|   ├── vitalsigns_screen.py
|   ├── mood_screen.py
|   └── logout_screen.py
├── __init__.py
├── assets/
└── app.py

1. Python (version 3.10+ recommended)
2. customtkinter
3. pillow
4. python-dotenv
5. supabase
6. (Optional, but recommended) pip for package management

You can install the Python packages using:
└── app.pypip install customtkinter pillow python-dotenv supabase

Make sure to also have your .env file with the required Supabase credentials.
