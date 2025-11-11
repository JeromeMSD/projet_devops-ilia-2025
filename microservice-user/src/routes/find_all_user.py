class UserNotFoundError(Exception):
    """Exception levée quand un utilisateur n'est pas trouvé"""
    pass


class User:
    """Classe représentant un utilisateur"""
    
    def __init__(self, identifiant: int, nom: str, prenom: str, role: str):
        self.identifiant = identifiant
        self.nom = nom
        self.prenom = prenom
        self.role = role
    
    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire"""
        return {
            "identifiant": self.identifiant,
            "nom": self.nom,
            "prenom": self.prenom,
            "role": self.role
        }
    
    def __repr__(self):
        return f"User(id={self.identifiant}, nom={self.nom}, prenom={self.prenom}, role={self.role})"


class UserRepository:
    """Repository pour gérer les utilisateurs en mémoire"""
    
    def __init__(self):
        self._users = {}
    
    def add(self, user: User):
        """Ajoute un utilisateur au repository"""
        self._users[user.identifiant] = user
    
    def get_by_id(self, identifiant: int) -> User:
        """Récupère un utilisateur par son identifiant
        
        Args:
            identifiant: L'identifiant de l'utilisateur
            
        Returns:
            L'utilisateur trouvé
            
        Raises:
            UserNotFoundError: Si l'utilisateur n'existe pas
        """
        if identifiant not in self._users:
            raise UserNotFoundError(f"Utilisateur avec l'identifiant {identifiant} non trouvé")
        
        return self._users[identifiant]
    
    def get_all(self):
        """Retourne tous les utilisateurs"""
        return list(self._users.values())
    
    def update(self, user: User):
        """Met à jour un utilisateur existant
        
        Args:
            user: L'utilisateur avec les nouvelles données
            
        Raises:
            UserNotFoundError: Si l'utilisateur n'existe pas
        """
        if user.identifiant not in self._users:
            raise UserNotFoundError(f"Utilisateur avec l'identifiant {user.identifiant} non trouvé")
        
        self._users[user.identifiant] = user
    
    def delete(self, identifiant: int):
        """Supprime un utilisateur
        
        Args:
            identifiant: L'identifiant de l'utilisateur à supprimer
            
        Raises:
            UserNotFoundError: Si l'utilisateur n'existe pas
        """
        if identifiant not in self._users:
            raise UserNotFoundError(f"Utilisateur avec l'identifiant {identifiant} non trouvé")
        
        del self._users[identifiant]