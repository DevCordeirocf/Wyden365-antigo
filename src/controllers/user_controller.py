from src.services.auth_service import AuthService
from src.models.user import User

class UserController:
    @staticmethod
    def register_user(name, email, password, favorite_team):
        user = AuthService.register(name, email, password, favorite_team)
        return user

    @staticmethod
    def login_user(email, password):
        user = AuthService.login(email, password)
        return user
