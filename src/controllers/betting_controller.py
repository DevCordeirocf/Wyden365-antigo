"""
BettingController - Gerencia o fluxo de apostas
Orquestra as validações de saldo, regras de apostas e processamento
"""

from services.betting_service import BettingService
from services.wallet_service import WalletService
from services.event_service import EventService


class BettingController:
    def __init__(self):
        """Inicializa o controller com os serviços necessários"""
        self.betting_service = BettingService()
        self.wallet_service = WalletService()
        self.event_service = EventService()
    
    def place_bet(self, user_id, event_id, team_id, amount):
        """
        Processa uma nova aposta
        
        Args:
            user_id (int): ID do usuário
            event_id (int): ID do evento
            team_id (str): Time apostado ("team1", "team2" ou "draw")
            amount (float): Valor da aposta
        
        Returns:
            dict: {"success": bool, "message": str, "bet_id": int}
        """
        try:
            # 1. Valida se o valor da aposta é válido
            if amount <= 0:
                return {
                    "success": False,
                    "message": "O valor da aposta deve ser maior que zero"
                }
            
            # 2. Verifica se o evento existe e está disponível
            event_result = self.event_service.get_event_by_id(event_id)
            
            if not event_result["success"]:
                return {
                    "success": False,
                    "message": "Evento não encontrado"
                }
            
            # 3. Verifica se o evento ainda está aberto para apostas
            event = event_result["event"]
            if not self.event_service.is_event_open_for_betting(event):
                return {
                    "success": False,
                    "message": "Este evento não está mais disponível para apostas"
                }
            
            # 4. Verifica se o usuário tem saldo suficiente
            balance_check = self.wallet_service.has_sufficient_balance(user_id, amount)
            
            if not balance_check["success"] or not balance_check["has_balance"]:
                current_balance = balance_check.get("current_balance", 0)
                return {
                    "success": False,
                    "message": f"Saldo insuficiente. Saldo atual: R$ {current_balance:.2f}"
                }
            
            # 5. Bloqueia o valor na carteira
            block_result = self.wallet_service.block_balance(user_id, amount)
            
            if not block_result["success"]:
                return block_result
            
            # 6. Registra a aposta
            bet_result = self.betting_service.create_bet(
                user_id=user_id,
                event_id=event_id,
                team_id=team_id,
                amount=amount
            )
            
            if bet_result["success"]:
                return {
                    "success": True,
                    "message": "Aposta realizada com sucesso!",
                    "bet_id": bet_result.get("bet_id")
                }
            else:
                # Se falhar ao criar a aposta, devolve o dinheiro
                self.wallet_service.deposit(user_id, amount)
                return {
                    "success": False,
                    "message": "Erro ao processar aposta. Valor devolvido."
                }
            
        except Exception as e:
            # Em caso de erro, tenta devolver o dinheiro
            try:
                self.wallet_service.deposit(user_id, amount)
            except:
                pass
            
            return {
                "success": False,
                "message": f"Erro ao realizar aposta: {str(e)}"
            }
    
    def get_user_bets(self, user_id, active_only=False):
        """
        Lista as apostas de um usuário
        
        Args:
            user_id (int): ID do usuário
            active_only (bool): Se True, retorna apenas apostas ativas
        
        Returns:
            dict: {"success": bool, "bets": list}
        """
        try:
            result = self.betting_service.get_user_bets(user_id, active_only)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar apostas: {str(e)}",
                "bets": []
            }
    
    def get_bet_details(self, bet_id, user_id):
        """
        Busca detalhes de uma aposta específica
        
        Args:
            bet_id (int): ID da aposta
            user_id (int): ID do usuário (para validação)
        
        Returns:
            dict: {"success": bool, "bet": dict, "event": dict}
        """
        try:
            # Busca a aposta
            bet_result = self.betting_service.get_bet_by_id(bet_id)
            
            if not bet_result["success"]:
                return bet_result
            
            bet = bet_result["bet"]
            
            # Verifica se a aposta pertence ao usuário
            if bet["userid"] != user_id:
                return {
                    "success": False,
                    "message": "Você não tem permissão para ver esta aposta"
                }
            
            # Busca informações do evento
            event_result = self.event_service.get_event_by_id(bet["eventid"])
            
            return {
                "success": True,
                "bet": bet,
                "event": event_result.get("event", {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar detalhes: {str(e)}"
            }
    
    def get_user_betting_summary(self, user_id):
        """
        Retorna um resumo das apostas do usuário
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            dict: Resumo com estatísticas de apostas
        """
        try:
            # Busca todas as apostas do usuário
            bets_result = self.betting_service.get_user_bets(user_id, active_only=False)
            
            if not bets_result["success"]:
                return bets_result
            
            bets = bets_result.get("bets", [])
            
            # Calcula estatísticas
            total_bets = len(bets)
            total_amount_bet = sum(bet["amount"] for bet in bets)
            active_bets = len([bet for bet in bets if not bet.get("settled", False)])
            
            # Busca apostas vencedoras (se houver campo settled)
            won_bets = len([bet for bet in bets if bet.get("won", False)])
            
            return {
                "success": True,
                "summary": {
                    "total_bets": total_bets,
                    "active_bets": active_bets,
                    "won_bets": won_bets,
                    "total_amount_bet": total_amount_bet
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao gerar resumo: {str(e)}"
            }
    
    def cancel_bet(self, bet_id, user_id):
        """
        Cancela uma aposta (apenas se o evento ainda não começou)
        
        Args:
            bet_id (int): ID da aposta
            user_id (int): ID do usuário
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            # Busca a aposta
            bet_result = self.betting_service.get_bet_by_id(bet_id)
            
            if not bet_result["success"]:
                return bet_result
            
            bet = bet_result["bet"]
            
            # Verifica se pertence ao usuário
            if bet["userid"] != user_id:
                return {
                    "success": False,
                    "message": "Você não pode cancelar esta aposta"
                }
            
            # Verifica se o evento ainda não começou
            event_result = self.event_service.get_event_by_id(bet["eventid"])
            
            if not event_result["success"]:
                return event_result
            
            event = event_result["event"]
            
            if not self.event_service.is_event_open_for_betting(event):
                return {
                    "success": False,
                    "message": "Não é possível cancelar. O evento já começou."
                }
            
            # Cancela a aposta
            cancel_result = self.betting_service.cancel_bet(bet_id)
            
            if not cancel_result["success"]:
                return cancel_result
            
            # Devolve o dinheiro
            refund_result = self.wallet_service.deposit(user_id, bet["amount"])
            
            if refund_result["success"]:
                return {
                    "success": True,
                    "message": f"Aposta cancelada. R$ {bet['amount']:.2f} devolvido à carteira."
                }
            else:
                return {
                    "success": False,
                    "message": "Aposta cancelada, mas erro ao devolver o dinheiro. Contate o suporte."
                }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao cancelar aposta: {str(e)}"
            }
    
    def get_event_odds(self, event_id):
        """
        Retorna as odds (cotações) de um evento
        
        Args:
            event_id (int): ID do evento
        
        Returns:
            dict: {"success": bool, "odds": dict}
        """
        try:
            result = self.betting_service.get_event_odds(event_id)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar odds: {str(e)}"
            }