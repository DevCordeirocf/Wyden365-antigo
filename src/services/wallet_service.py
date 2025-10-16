from supabase import create_client, Client
import os
from dotenv import load_dotenv
from src.models.wallet import Wallet

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class WalletService:
    @staticmethod
    def get_user_wallet(userid):
        try:
            response = supabase.table("wallet").select("*").eq("userid", userid).execute()
            if response.data:
                return Wallet.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao buscar carteira do usuário: {e}")
            return None

    @staticmethod
    def create_wallet(userid, initial_balance=0.0):
        try:
            wallet_data = {
                "userid": userid,
                "balance": initial_balance
            }
            response = supabase.table("wallet").insert(wallet_data).execute()
            if response.data:
                return Wallet.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao criar carteira para o usuário: {e}")
            return None

    @staticmethod
    def update_balance(userid, amount):
        try:
            # Primeiro, obtenha a carteira atual
            current_wallet = WalletService.get_user_wallet(userid)
            if not current_wallet:
                # Se não existir, crie uma nova carteira
                current_wallet = WalletService.create_wallet(userid)
                if not current_wallet:
                    return None # Falha ao criar carteira

            new_balance = current_wallet.balance + amount
            if new_balance < 0:
                print("Erro: Saldo insuficiente.")
                return None

            response = supabase.table("wallet").update({"balance": new_balance}).eq("userid", userid).execute()
            if response.data:
                return Wallet.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao atualizar saldo da carteira: {e}")
            return None
