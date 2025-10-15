from database import get_supabase_client


class WalletService:
    def __init__(self):
        """Inicializa o serviço com a conexão ao Supabase"""
        self.supabase = get_supabase_client()
    
    def create_wallet(self, user_id, initial_balance=0.0):
        """
        Cria uma carteira para um novo usuário
        
        Args:
            user_id (int): ID do usuário
            initial_balance (float): Saldo inicial (padrão: 0.0)
        
        Returns:
            dict: {"success": bool, "message": str, "wallet_id": int}
        """
        try:
            # Verifica se o usuário já tem carteira
            existing = self.supabase.table("wallet").select("*").eq("userid", user_id).execute()
            
            if existing.data:
                return {
                    "success": False,
                    "message": "Usuário já possui uma carteira"
                }
            
            # Cria nova carteira
            wallet_data = {
                "userid": user_id,
                "balance": initial_balance
            }
            
            result = self.supabase.table("wallet").insert(wallet_data).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Carteira criada com sucesso",
                    "wallet_id": result.data[0]["id"]
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao criar carteira"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao criar carteira: {str(e)}"
            }
    
    def get_balance(self, user_id):
        """
        Consulta o saldo atual da carteira do usuário
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            dict: {"success": bool, "wallet": dict, "balance": float}
        """
        try:
            result = self.supabase.table("wallet").select("*").eq("userid", user_id).execute()
            
            if result.data:
                wallet = result.data[0]
                return {
                    "success": True,
                    "wallet": wallet,
                    "balance": wallet["balance"]
                }
            else:
                return {
                    "success": False,
                    "message": "Carteira não encontrada"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao consultar saldo: {str(e)}"
            }
    
    def deposit(self, user_id, amount):
        """
        Realiza um depósito na carteira do usuário
        
        Args:
            user_id (int): ID do usuário
            amount (float): Valor a ser depositado
        
        Returns:
            dict: {"success": bool, "message": str, "new_balance": float}
        """
        try:
            # Validação: valor deve ser positivo
            if amount <= 0:
                return {
                    "success": False,
                    "message": "O valor do depósito deve ser maior que zero"
                }
            
            # Busca saldo atual
            wallet_result = self.get_balance(user_id)
            
            if not wallet_result["success"]:
                return wallet_result
            
            current_balance = wallet_result["balance"]
            new_balance = current_balance + amount
            
            # Atualiza saldo
            update_result = self.supabase.table("wallet").update({
                "balance": new_balance
            }).eq("userid", user_id).execute()
            
            if update_result.data:
                return {
                    "success": True,
                    "message": f"Depósito de R$ {amount:.2f} realizado com sucesso",
                    "new_balance": new_balance
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao processar depósito"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao realizar depósito: {str(e)}"
            }
    
    def withdraw(self, user_id, amount):
        """
        Realiza um saque da carteira do usuário
        
        Args:
            user_id (int): ID do usuário
            amount (float): Valor a ser sacado
        
        Returns:
            dict: {"success": bool, "message": str, "new_balance": float}
        """
        try:
            # Validação: valor deve ser positivo
            if amount <= 0:
                return {
                    "success": False,
                    "message": "O valor do saque deve ser maior que zero"
                }
            
            # Busca saldo atual
            wallet_result = self.get_balance(user_id)
            
            if not wallet_result["success"]:
                return wallet_result
            
            current_balance = wallet_result["balance"]
            
            # Validação: saldo suficiente
            if current_balance < amount:
                return {
                    "success": False,
                    "message": f"Saldo insuficiente. Saldo atual: R$ {current_balance:.2f}"
                }
            
            new_balance = current_balance - amount
            
            # Atualiza saldo
            update_result = self.supabase.table("wallet").update({
                "balance": new_balance
            }).eq("userid", user_id).execute()
            
            if update_result.data:
                return {
                    "success": True,
                    "message": f"Saque de R$ {amount:.2f} realizado com sucesso",
                    "new_balance": new_balance
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao processar saque"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao realizar saque: {str(e)}"
            }
    
    def has_sufficient_balance(self, user_id, amount):
        """
        Verifica se o usuário tem saldo suficiente
        
        Args:
            user_id (int): ID do usuário
            amount (float): Valor a ser verificado
        
        Returns:
            dict: {"success": bool, "has_balance": bool, "current_balance": float}
        """
        try:
            wallet_result = self.get_balance(user_id)
            
            if not wallet_result["success"]:
                return {
                    "success": False,
                    "has_balance": False,
                    "message": "Erro ao verificar saldo"
                }
            
            current_balance = wallet_result["balance"]
            has_balance = current_balance >= amount
            
            return {
                "success": True,
                "has_balance": has_balance,
                "current_balance": current_balance
            }
            
        except Exception as e:
            return {
                "success": False,
                "has_balance": False,
                "message": f"Erro ao verificar saldo: {str(e)}"
            }
    
    def block_balance(self, user_id, amount):
        """
        Bloqueia um valor da carteira (usado quando uma aposta é feita)
        
        Args:
            user_id (int): ID do usuário
            amount (float): Valor a ser bloqueado
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            # Verifica se tem saldo suficiente
            check_result = self.has_sufficient_balance(user_id, amount)
            
            if not check_result["success"] or not check_result["has_balance"]:
                return {
                    "success": False,
                    "message": "Saldo insuficiente para bloquear"
                }
            
            # Deduz o valor do saldo (simula bloqueio)
            return self.withdraw(user_id, amount)
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao bloquear saldo: {str(e)}"
            }
    
    def add_prize(self, user_id, prize_amount):
        """
        Adiciona o prêmio de uma aposta vencedora à carteira
        
        Args:
            user_id (int): ID do usuário
            prize_amount (float): Valor do prêmio
        
        Returns:
            dict: {"success": bool, "message": str, "new_balance": float}
        """
        try:
            return self.deposit(user_id, prize_amount)
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao adicionar prêmio: {str(e)}"
            }
    
    def get_transaction_history(self, user_id, limit=10):
        """
        Retorna o histórico de transações da carteira
        (Esta função pode ser expandida se você criar uma tabela de transações)
        
        Args:
            user_id (int): ID do usuário
            limit (int): Número máximo de transações a retornar
        
        Returns:
            dict: {"success": bool, "transactions": list}
        """
        try:
            # Por enquanto, retorna apenas o saldo atual
            # Você pode criar uma tabela 'transactions' no futuro para histórico completo
            wallet_result = self.get_balance(user_id)
            
            if not wallet_result["success"]:
                return {
                    "success": False,
                    "transactions": []
                }
            
            return {
                "success": True,
                "transactions": [],  # Implementar quando criar tabela de transações
                "message": "Funcionalidade de histórico será implementada"
            }
            
        except Exception as e:
            return {
                "success": False,
                "transactions": [],
                "message": f"Erro ao buscar histórico: {str(e)}"
            }