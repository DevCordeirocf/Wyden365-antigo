# betting_service.py
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from src.models.bet import Bet
from src.models.event import Event

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class BettingService:
    @staticmethod
    def place_bet(userid, eventid, selected_team, amount, odds, potential_prize):
        try:
            bet_data = {
                "userid": userid,
                "eventid": eventid,
                "selected_team": selected_team,
                "amount": amount,
                "odds": odds,
                "potential_prize": potential_prize,
                "status": "pending"
            }
            response = supabase.table("bet").insert(bet_data).execute()
            if response.data:
                return Bet.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao fazer a aposta: {e}")
            return None

    @staticmethod
    def get_user_bets(userid):
        try:
            response = supabase.table("bet").select("*, event(*)").eq("userid", userid).execute()
            if response.data:
                bets = []
                for bet_data in response.data:
                    bet = Bet.from_dict(bet_data)
                    # Ensure event data is correctly mapped to an Event object
                    if 'event' in bet_data and bet_data['event'] is not None:
                        bet.event = Event.from_dict(bet_data['event'])
                    else:
                        bet.event = None # Or handle as appropriate if event can be null
                    bets.append(bet)
                return bets
            return []
        except Exception as e:
            print(f"Erro ao buscar apostas do usuário: {e}")
            return []

    @staticmethod
    def get_event_bets(eventid):
        try:
            response = supabase.table("bet").select("*").eq("eventid", eventid).execute()
            if response.data:
                return [Bet.from_dict(bet) for bet in response.data]
            return []
        except Exception as e:
            print(f"Erro ao buscar apostas do evento: {e}")
            return None

    @staticmethod
    def update_bet_status(betid, status, prize_amount=None):
        try:
            update_data = {"status": status}
            if prize_amount is not None:
                update_data["potential_prize"] = prize_amount

            response = supabase.table("bet").update(update_data).eq("id", betid).execute()
            if response.data:
                return Bet.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao atualizar status da aposta: {e}")
            return None
