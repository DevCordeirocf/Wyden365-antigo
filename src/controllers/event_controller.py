from services.event_service import EventService
from services.betting_service import BettingService
from services.wallet_service import WalletService


class EventController:
    def __init__(self):
        """Inicializa o controller com os serviços necessários"""
        self.event_service = EventService()
        self.betting_service = BettingService()
        self.wallet_service = WalletService()
    
    def create_event(self, sport, team1, team2, date, admin_id):
        """
        Cria um novo evento esportivo (apenas para administradores)
        
        Args:
            sport (str): Tipo de esporte (ex: "futebol", "basquete")
            team1 (str): Nome do time 1
            team2 (str): Nome do time 2
            date (datetime): Data e hora do evento
            admin_id (int): ID do administrador que está criando
        
        Returns:
            dict: {"success": bool, "message": str, "event_id": int}
        """
        try:
            # Delega a criação para o EventService
            result = self.event_service.create_event(sport, team1, team2, date)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao criar evento: {str(e)}"
            }
    
    def get_available_events(self):
        """
        Lista todos os eventos disponíveis para apostas (não finalizados)
        
        Returns:
            dict: {"success": bool, "events": list}
        """
        try:
            result = self.event_service.get_available_events()
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao listar eventos: {str(e)}",
                "events": []
            }
    
    def get_event_by_id(self, event_id):
        """
        Busca um evento específico pelo ID
        
        Args:
            event_id (int): ID do evento
        
        Returns:
            dict: {"success": bool, "event": dict}
        """
        try:
            result = self.event_service.get_event_by_id(event_id)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar evento: {str(e)}"
            }
    
    def finalize_event(self, event_id, winner_team, admin_id):
        """
        Finaliza um evento e distribui os prêmios
        (apenas para administradores)
        
        Args:
            event_id (int): ID do evento
            winner_team (str): Time vencedor ("team1", "team2" ou "draw")
            admin_id (int): ID do administrador
        
        Returns:
            dict: {"success": bool, "message": str, "winners_count": int}
        """
        try:
            # 1. Finaliza o evento no EventService
            finalize_result = self.event_service.finalize_event(event_id, winner_team)
            
            if not finalize_result["success"]:
                return finalize_result
            
            # 2. Busca todas as apostas vencedoras deste evento
            winners_result = self.betting_service.get_winning_bets(event_id, winner_team)
            
            if not winners_result["success"]:
                return {
                    "success": False,
                    "message": "Evento finalizado, mas erro ao buscar apostas vencedoras"
                }
            
            winning_bets = winners_result.get("bets", [])
            
            # 3. Distribui os prêmios para cada vencedor
            winners_count = 0
            for bet in winning_bets:
                prize_amount = bet["amount"] * bet.get("odds", 2.0)  # valor * odd
                
                prize_result = self.wallet_service.add_prize(
                    user_id=bet["userid"],
                    prize_amount=prize_amount
                )
                
                if prize_result["success"]:
                    winners_count += 1
            
            return {
                "success": True,
                "message": f"Evento finalizado! {winners_count} apostadores premiados.",
                "winners_count": winners_count
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao finalizar evento: {str(e)}"
            }
    
    def get_event_statistics(self, event_id):
        """
        Retorna estatísticas de um evento (total apostado, número de apostas, etc)
        
        Args:
            event_id (int): ID do evento
        
        Returns:
            dict: {"success": bool, "statistics": dict}
        """
        try:
            # Busca informações do evento
            event_result = self.event_service.get_event_by_id(event_id)
            
            if not event_result["success"]:
                return event_result
            
            # Busca estatísticas de apostas
            stats_result = self.betting_service.get_event_betting_stats(event_id)
            
            return {
                "success": True,
                "statistics": {
                    "event": event_result["event"],
                    "betting_stats": stats_result.get("stats", {})
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar estatísticas: {str(e)}"
            }
    
    def get_finished_events(self, limit=20):
        """
        Lista eventos já finalizados (histórico)
        
        Args:
            limit (int): Número máximo de eventos a retornar
        
        Returns:
            dict: {"success": bool, "events": list}
        """
        try:
            result = self.event_service.get_finished_events(limit)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar histórico: {str(e)}",
                "events": []
            }
    
    def cancel_event(self, event_id, admin_id):
        """
        Cancela um evento e devolve o dinheiro das apostas
        (apenas para administradores)
        
        Args:
            event_id (int): ID do evento
            admin_id (int): ID do administrador
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            # 1. Busca todas as apostas deste evento
            bets_result = self.betting_service.get_bets_by_event(event_id)
            
            if not bets_result["success"]:
                return bets_result
            
            bets = bets_result.get("bets", [])
            
            # 2. Devolve o dinheiro de cada aposta
            refunded_count = 0
            for bet in bets:
                refund_result = self.wallet_service.deposit(
                    user_id=bet["userid"],
                    amount=bet["amount"]
                )
                
                if refund_result["success"]:
                    refunded_count += 1
            
            # 3. Cancela/deleta o evento
            cancel_result = self.event_service.cancel_event(event_id)
            
            if cancel_result["success"]:
                return {
                    "success": True,
                    "message": f"Evento cancelado. {refunded_count} apostas reembolsadas."
                }
            else:
                return {
                    "success": False,
                    "message": "Apostas reembolsadas, mas erro ao cancelar evento"
                }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao cancelar evento: {str(e)}"
            }