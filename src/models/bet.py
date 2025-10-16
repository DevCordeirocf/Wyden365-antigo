
class Bet:
    def __init__(self, id, userid, eventid, selected_team, amount, odds, potential_prize, status, created_at):
        self.id = id
        self.userid = userid
        self.eventid = eventid
        self.selected_team = selected_team
        self.amount = amount
        self.odds = odds
        self.potential_prize = potential_prize
        self.status = status
        self.created_at = created_at

    @staticmethod
    def from_dict(data):
        return Bet(
            data.get("id"),
            data.get("userid"),
            data.get("eventid"),
            data.get("selected_team"),
            data.get("amount"),
            data.get("odds"),
            data.get("potential_prize"),
            data.get("status"),
            data.get("created_at")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "eventid": self.eventid,
            "selected_team": self.selected_team,
            "amount": self.amount,
            "odds": self.odds,
            "potential_prize": self.potential_prize,
            "status": self.status,
            "created_at": self.created_at
        }
