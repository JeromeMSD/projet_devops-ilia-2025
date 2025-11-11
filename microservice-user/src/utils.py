import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone
import uuid

from dotenv import load_dotenv

load_dotenv()

# constantes.
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ENCODER_TYPE = 'utf-8'
ALGORITHM = 'HS256'


def hash_password(password: str) -> str:
    """
        Cette fonction permet de hasher une chaine de caractère en utilisant l'algorithme bcrypt.
        Args:
            password (str): La chaîne de caractères à hasher (mot de passe en clair).
        Raise:
            Leve une exception en cas de pépins
        Returns:
            str: Le mot de passe haché et encodé en chaîne de caractères.
    """
    try:
        return bcrypt.hashpw(password.encode(ENCODER_TYPE), bcrypt.gensalt()).decode(ENCODER_TYPE)
    except Exception as error:
        print(f"erreur durant l'opération de hash du mot de passe {error}")
        raise error


def verify_password(password: str, hashed_password: str) -> bool:
    """
        Cette fonction permet de verifier que deux chaines caractères possèdent le meme hash, garantissant que les deux chaines
        de caractères sont identiques.
        Args:
            password (str): Mot de passe en clair.
            hashed_password (str): Mot de passe hash
        Raise:
            Leve une exception en cas de pépins
        Returns:
            bool: True si les deux chaines sont égales et False sinon
    """
    try:
        return bcrypt.checkpw(password.encode(ENCODER_TYPE), hashed_password.encode(ENCODER_TYPE))
    except Exception as error:
        print(f"erreur durant la verification du mot de passe {error}")
        raise error


def create_token(user_id: str | bytes, user_role: str = "", validity: timedelta = timedelta(hours=24)) -> str:
    """
        Fonction utilitaire permettant de créer un JWT Token pour sécuriser les sessions et les communications
        Args:
            validity (timedelta) : durée de la validité du token
            user_role (str) : Role de l'utilisateur
            user_id (str) : id d'un utilisateur
        Return:
            str: JWT Token
        Raise:
            Exception: Leve une Exception en cas de soucis
    """
    try:
        payload: dict = {
            'id_user': user_id.decode(ENCODER_TYPE) if isinstance(user_id, bytes) else str(user_id),
            'role': user_role,
            'exp': datetime.now(timezone.utc) + validity,
            'iat': datetime.now(timezone.utc),
            'jti': str(uuid.uuid4())
        }
        return jwt.encode(
            payload=payload,
            key=SECRET_KEY,
            algorithm=ALGORITHM)
    except Exception as error:
        raise error


def decode_token(token: str, disable_exp_verification: bool = False) -> dict:
    """
        Fonction utilitaire permettant de decoder un JWT Token
        Args:
            token (str) : token de session d'un utilisateur
            disable_exp_verification:
        Return:
            dict: Retourne un tableau cle valeur donnant les informations du token
        Raise:
            Exception: Leve une Exception en cas de soucis
    """
    try:
        return jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": not disable_exp_verification},
        )
    except jwt.DecodeError:
        raise jwt.DecodeError
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except Exception as error:
        raise RuntimeError("Error lors du décodage du token", error)


def verify_token(token: str) -> dict | str | None:
    """
        Fonction utilitaire permettant de decoder un JWT Token afin de verifier son intégrité, sa validité
        Args:
            token (str) : token de session d'un utilisateur
        Return:
            dict: Retourne un tableau cle valeur donnant les informations du token
        Raise :
            – Return id_user (str) : en cas de token expiree, retourne l'id de l'utilisateur
            — propage les erreurs DecodeError, InvalidTokenError et Exception en cas de soucis lors du décodage du token et retourne None
    """
    try:
        decoded_token: dict = decode_token(token=token, disable_exp_verification=False)
        return decoded_token
    except jwt.ExpiredSignatureError as error:
        print(f"Token expiré : {error}")
        try:
            expired_payload: dict = decode_token(token=token, disable_exp_verification=True)
            return expired_payload.get('id_user')
        except Exception as error:
            print(f"Erreur lors du décodage du token expiré: {error}")
            raise error
    except jwt.DecodeError as error:
        print(f"Erreur de décodage: {error}")
        raise error
    except jwt.InvalidTokenError as error:
        print(f"Token invalide: {error}")
        raise error
    except Exception as error:
        print(f"Erreur inattendue: {error}")
        raise error
