from services.auth_service import AuthService
from services.wallet_service import WalletService


class UserController:
    def __init__(self):
        """Inicializa o controller com os serviços necessários"""
        self.auth_service = AuthService()
        self.wallet_service = WalletService()
    
    def register_user(self, name, email, password, favorite_team=None):
        """
        Registra um novo usuário no sistema
        
        Args:
            name (str): Nome do usuário
            email (str): Email do usuário
            password (str): Senha do usuário
            favorite_team (str, optional): Time favorito do usuário
        
        Returns:
            dict: {"success": bool, "message": str, "user_id": int (se sucesso)}
        """
        try:
            # Delega o registro para o AuthService
            result = self.auth_service.register(name, email, password, favorite_team)
            
            if result["success"]:
                # Cria a carteira inicial para o usuário
                user_id = result["user_id"]
                wallet_result = self.wallet_service.create_wallet(user_id)
                
                if wallet_result["success"]:
                    return {
                        "success": True,
                        "message": "Usuário registrado com sucesso!",
                        "user_id": user_id
                    }
                else:
                    return {
                        "success": False,
                        "message": "Usuário criado, mas erro ao criar carteira."
                    }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao registrar usuário: {str(e)}"
            }
    
    def login_user(self, email, password):
        """
        Realiza o login do usuário
        
        Args:
            email (str): Email do usuário
            password (str): Senha do usuário
        
        Returns:
            dict: {"success": bool, "message": str, "user": dict (se sucesso)}
        """
        try:
            # Delega a autenticação para o AuthService
            result = self.auth_service.login(email, password)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao fazer login: {str(e)}"
            }
    
    def get_user_profile(self, user_id):
        """
        Busca o perfil completo do usuário, incluindo saldo
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            dict: {"success": bool, "user": dict, "wallet": dict}
        """
        try:
            # Busca dados do usuário
            user_result = self.auth_service.get_user_by_id(user_id)
            
            if not user_result["success"]:
                return user_result
            
            # Busca saldo da carteira
            wallet_result = self.wallet_service.get_balance(user_id)
            
            return {
                "success": True,
                "user": user_result["user"],
                "wallet": wallet_result.get("wallet", {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao buscar perfil: {str(e)}"
            }
    
    def update_favorite_team(self, user_id, favorite_team):
        """
        Atualiza o time favorito do usuário
        
        Args:
            user_id (int): ID do usuário
            favorite_team (str): Nome do time favorito
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            result = self.auth_service.update_favorite_team(user_id, favorite_team)
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao atualizar time favorito: {str(e)}"
            }
    
    def check_is_admin(self, user_id):
        """
        Verifica se o usuário é administrador
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            bool: True se for admin, False caso contrário
        """
        try:
            result = self.auth_service.is_admin(user_id)
            return result.get("is_admin", False)
            
        except Exception as e:
            return False
    
    def get_user_dashboard_data(self, user_id):
        """
        Retorna todos os dados necessários para o dashboard do usuário
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            dict: Dados completos do dashboard
        """
        try:
            # Busca perfil completo
            profile = self.get_user_profile(user_id)
            
            if not profile["success"]:
                return profile
            
            # Busca histórico de transações
            transactions = self.wallet_service.get_transaction_history(user_id)
            
            return {
                "success": True,
                "user": profile["user"],
                "wallet": profile["wallet"],
                "transactions": transactions.get("transactions", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao carregar dashboard: {str(e)}"
            }