from src.services.wallet_service import WalletService
from src.models.wallet import Wallet

class WalletController:
    @staticmethod
    def get_user_wallet(userid):
        return WalletService.get_user_wallet(userid)

    @staticmethod
    def update_balance(userid, amount):
        return WalletService.update_balance(userid, amount)

    @staticmethod
    def create_wallet_for_user(userid, initial_balance=0.0):
        return WalletService.create_wallet(userid, initial_balance)
