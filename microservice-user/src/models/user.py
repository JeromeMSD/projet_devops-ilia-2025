"""
User model for the microservice-user API
"""
from datetime import datetime


class User:
    """
    User model representing a user in the system
    """

    def __init__(self, username, email, password_hash, role="user", user_id=None, created_at=None):
        self.user_id = user_id or f"USR-{int(datetime.now().timestamp())}"
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role  # user, sre, admin
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self, include_password=False):
        """
        Convert user object to dictionary
        """
        user_dict = {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

        if include_password:
            user_dict["password_hash"] = self.password_hash

        return user_dict

    @staticmethod
    def from_dict(data):
        """
        Create a User object from a dictionary
        """
        return User(
            username=data.get("username"),
            email=data.get("email"),
            password_hash=data.get("password_hash"),
            role=data.get("role", "user"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at")
        )

    def validate(self):
        """
        Validate user data
        """
        errors = []

        if not self.username or len(self.username) < 3:
            errors.append("Username must be at least 3 characters long")

        if not self.email or "@" not in self.email:
            errors.append("Invalid email address")

        if self.role not in ["user", "sre", "admin"]:
            errors.append("Role must be one of: user, sre, admin")

        return len(errors) == 0, errors
