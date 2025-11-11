<<<<<<< HEAD
class UserNotFoundError(Exception):
    """Exception levée quand un utilisateur n'est pas trouvé"""
    pass
=======
from flask import Blueprint, jsonify
from flask_cors import cross_origin
import redis

from ..auth import auth_required
from ..models.user import User
from src.redis_client import get_redis_client
>>>>>>> origin/Microservice-USER


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


<<<<<<< HEAD
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
=======
@get_all_users_bp.route(rule= '/users', methods=['GET'])
@cross_origin()
@auth_required(roles=['ADMIN', 'SRE'])
def find_all_users():
    """
    Route pour récupérer tous les utilisateurs stockés dans Redis.

    Returns:
        JSON: Liste de tous les utilisateurs avec leur nombre total

    Responses :
        200: Liste des utilisateurs récupérée avec succès
        500: Erreur serveur (problème Redis ou autre)
    """
    try:
        # Obtenir le client Redis
        redis_client = get_redis_client()

        # Vérifier la connexion Redis
        if redis_client is None:
            return jsonify({
                "error": "Database connection unavailable"
            }), 500

        # Récupérer toutes les clés des utilisateurs
        # Pattern: tous les utilisateurs ont des clés qui commencent par "user:"
        user_keys = redis_client.keys('user:*')

        users_list = []

        # Parcourir toutes les clés et récupérer les utilisateurs
        for key in user_keys:
            try:
                # Récupérer l'objet user depuis Redis (bytes)
                user_data = redis_client.get(key)

                if user_data:
                    # Convertir de Redis vers objet User
                    user = User.from_redis_to_user(user_data)
                    # Ajouter la version JSON (sans password) à la liste
                    users_list.append(user.to_json())

            except Exception as e:
                print(f"Erreur lors de la récupération de l'utilisateur {key}: {e}")
                continue

        # Retourner la liste avec le nombre total
        return jsonify({
            "count": len(users_list),
            "users": users_list
        }), 200

    except redis.ConnectionError:
        return jsonify({
            "error": "Cannot connect to database"
        }), 500

    except Exception as e:
        print(f"Erreur inattendue dans find_all_users: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500
>>>>>>> origin/Microservice-USER
