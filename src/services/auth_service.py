from supabase import create_client, Client
import os
from dotenv import load_dotenv
from src.models.user import User

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AuthService:
    @staticmethod
    def register(name, email, password, favorite_team):
        try:
            user_data = {
                "name": name,
                "email": email,
                "password": password, # Note: In a real app, hash passwords before storing
                "favorite_team": favorite_team,
                "is_admin": False
            }
            response = supabase.table("users").insert(user_data).execute()
            if response.data:
                return User.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return None

    @staticmethod
    def login(email, password):
        try:
            response = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
            if response.data:
                return User.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return None
