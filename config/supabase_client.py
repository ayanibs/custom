from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Verify the connection (optional)
try:
    # Test the connection by making a simple query
    response = supabase.table('students').select("*").limit(1).execute()
    print("Supabase connection successful!")
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}")