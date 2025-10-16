# event_service.py
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from src.models.event import Event

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class EventService:
    @staticmethod
    def create_event(sport, team1, team2, odds_team1, odds_team2, date, status="scheduled", winner=None):
        try:
            event_data = {
                "sport": sport,
                "team1": team1,
                "team2": team2,
                "odds_team1": odds_team1,
                "odds_team2": odds_team2,
                "date": date,
                "status": status,
                "winner": winner
            }
            response = supabase.table("event").insert(event_data).execute()
            if response.data:
                return Event.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao criar evento: {e}")
            return None

    @staticmethod
    def get_all_events():
        try:
            response = supabase.table("event").select("*").execute()
            if response.data:
                return [Event.from_dict(event) for event in response.data]
            return []
        except Exception as e:
            print(f"Erro ao buscar eventos: {e}")
            return []

    @staticmethod
    def update_event(event_id, sport=None, team1=None, team2=None, odds_team1=None, odds_team2=None, date=None, status=None, winner=None):
        try:
            update_data = {}
            if sport: update_data["sport"] = sport
            if team1: update_data["team1"] = team1
            if team2: update_data["team2"] = team2
            if odds_team1: update_data["odds_team1"] = odds_team1
            if odds_team2: update_data["odds_team2"] = odds_team2
            if date: update_data["date"] = date
            if status: update_data["status"] = status
            if winner: update_data["winner"] = winner

            response = supabase.table("event").update(update_data).eq("id", event_id).execute()
            if response.data:
                return Event.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao atualizar evento: {e}")
            return None

    @staticmethod
    def delete_event(event_id):
        try:
            response = supabase.table("event").delete().eq("id", event_id).execute()
            if response.data:
                return True
            return False
        except Exception as e:
            print(f"Erro ao deletar evento: {e}")
            return False
