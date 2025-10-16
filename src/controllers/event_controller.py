from src.services.event_service import EventService
from src.models.event import Event

class EventController:
    @staticmethod
    def create_event(sport, team1, team2, odds_team1, odds_team2, date, status="scheduled", winner=None):
        event = EventService.create_event(sport, team1, team2, odds_team1, odds_team2, date, status, winner)
        return event

    @staticmethod
    def get_all_events():
        events = EventService.get_all_events()
        return events

    @staticmethod
    def update_event(event_id, sport=None, team1=None, team2=None, odds_team1=None, odds_team2=None, date=None, status=None, winner=None):
        event = EventService.update_event(event_id, sport, team1, team2, odds_team1, odds_team2, date, status, winner)
        return event

    @staticmethod
    def delete_event(event_id):
        success = EventService.delete_event(event_id)
        return success
