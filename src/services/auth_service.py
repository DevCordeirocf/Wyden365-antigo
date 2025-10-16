from supabase import create_client, Client
import os
from dotenv import load_dotenv
from src.models.user import User
import bcrypt

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AuthService:
    @staticmethod
    def register(name, email, password, favorite_team):
        try:
            if isinstance(password, str):
                password_bytes = password.encode("utf-8")
            else:
                password_bytes = password

            hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

            user_data = {
                "name": name,
                "email": email,
                "password": hashed,
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
            # Fetch user by email and verify password against stored hash
            response = supabase.table("users").select("*").eq("email", email).execute()
            if response.data:
                user_row = response.data[0]
                stored_hash = user_row.get("password")
                if stored_hash is None:
                    return None

                if isinstance(password, str):
                    password_bytes = password.encode("utf-8")
                else:
                    password_bytes = password

                try:
                    stored_hash_bytes = stored_hash.encode("utf-8")
                except Exception:
                    stored_hash_bytes = stored_hash

                if bcrypt.checkpw(password_bytes, stored_hash_bytes):
                    return User.from_dict(user_row)
            return None
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return None
