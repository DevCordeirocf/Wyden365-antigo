class Wallet:
    def __init__(self, id, userid, balance, created_at):
        self.id = id
        self.userid = userid
        self.balance = balance
        self.created_at = created_at

    @staticmethod
    def from_dict(data):
        return Wallet(
            data.get("id"),
            data.get("userid"),
            data.get("balance"),
            data.get("created_at")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "balance": self.balance,
            "created_at": self.created_at
        }
