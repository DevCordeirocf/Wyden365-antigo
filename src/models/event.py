# event.py
class Event:
    def __init__(self, id, sport, team1, team2, odds_team1, odds_team2, date, status, winner, created_at):
        self.id = id
        self.sport = sport
        self.team1 = team1
        self.team2 = team2
        self.odds_team1 = odds_team1
        self.odds_team2 = odds_team2
        self.date = date
        self.status = status
        self.winner = winner
        self.created_at = created_at

    @staticmethod
    def from_dict(data):
        return Event(
            data.get('id'),
            data.get('sport'),
            data.get('team1'),
            data.get('team2'),
            data.get('odds_team1'),
            data.get('odds_team2'),
            data.get('date'),
            data.get('status'),
            data.get('winner'),
            data.get('created_at')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'sport': self.sport,
            'team1': self.team1,
            'team2': self.team2,
            'odds_team1': self.odds_team1,
            'odds_team2': self.odds_team2,
            'date': self.date,
            'status': self.status,
            'winner': self.winner,
            'created_at': self.created_at
        }
