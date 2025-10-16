from src.services.betting_service import BettingService

class BettingController:
    @staticmethod
    def place_bet(userid, eventid, selected_team, amount, odds, potential_prize):
        bet = BettingService.place_bet(userid, eventid, selected_team, amount, odds, potential_prize)
        return bet

    @staticmethod
    def get_user_bets(userid):
        bets = BettingService.get_user_bets(userid)
        return bets

    @staticmethod
    def update_bet_status(betid, status, prize_amount=None):
        bet = BettingService.update_bet_status(betid, status, prize_amount)
        return bet

    @staticmethod
    def get_winning_bets(eventid, winning_team):
        bets = BettingService.get_winning_bets(eventid, winning_team)
        return bets
