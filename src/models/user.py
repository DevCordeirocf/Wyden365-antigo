class User:
    def __init__(self, id, name, email, password, favorite_team, is_admin, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.favorite_team = favorite_team
        self.is_admin = is_admin
        self.created_at = created_at

    @staticmethod
    def from_dict(data):
        return User(
            data.get("id"),
            data.get("name"),
            data.get("email"),
            data.get("password"),
            data.get("favorite_team"),
            data.get("is_admin", False), # Default to False if not provided
            data.get("created_at")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "favorite_team": self.favorite_team,
            "is_admin": self.is_admin,
            "created_at": self.created_at
        }
