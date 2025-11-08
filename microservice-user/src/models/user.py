import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional




@dataclass
class User:
    """
        Modèle User représentant un utilisateur du système par:
        - Son id (uuid)
        - email (str)
        - password (str)
        - firstname (str)
        - lastname (str)
        Un utilisateur possède aussi un token (str) et cree a une date precise (datetime)
    """
    id_user: str
    firstname: str
    lastname: str
    email: str
    password: str
    token: Optional[str]
    created_at: Optional[datetime] = datetime.now(timezone.utc)




    def to_json(self) -> dict:
        """
            Convertit l'objet User en un dictionnaire prêt à être retourné par l'API (JSON-compatible).

            Cette méthode exclut les données sensibles (comme le mot de passe) et formate les
            objets datetime en chaînes de caractères.

            Args:
                self: L'instance de l'objet User.

            Returns:
                dict: Un dictionnaire représentant l'utilisateur, adapté pour une réponse HTTP JSON.
            """
        return {
            'id_user': self.id_user,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'token': self.token if self.token else "",
            'created_at': str(self.created_at)
        }


    def to_redis(self):
        """
            Sérialise l'objet User en une chaîne JSON prête à être stockée dans Redis.

            Cette méthode inclut toutes les données nécessaires à la persistance et à la vérification

            Args:
                self: L'instance de l'objet User.

            Returns:
                str: Une chaîne JSON sérialisée (type str), prête à être envoyée à la commande SET de Redis.
        """
        user_json = {
            "id_user": self.id_user,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
            "token" : self.token if self.token else "",
            "created_at": str(self.created_at)
        }
        return json.dumps(obj= user_json)



    @staticmethod
    def from_redis_to_user(redis_object: bytes) -> 'User':

        """
            Désérialise une chaîne de bytes (récupérée de Redis) en un objet User.
            Elle permet de construire un objet User à partir d'un objet de Redis.
            Args:
                redis_object (bytes) La chaîne d'octets bruts récupérée directement de la base de données Redis.
            Returns:
                User: Une nouvelle instance de la classe User.
        """

        string_obj: str = redis_object.decode("utf-8")
        json_obj: dict = json.loads(string_obj)
        return User(
            id_user=json_obj["id_user"],
            firstname=json_obj["firstname"],
            lastname=json_obj["lastname"],
            email=json_obj["email"],
            password=json_obj["password"],
            token=json_obj["token"],
            created_at=json_obj["created_at"]
        )






