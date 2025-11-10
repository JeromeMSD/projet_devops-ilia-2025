import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Redis connection configuration
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))



_redis_client = None


def get_redis_client():
    """
    Retourne une instance singleton du client Redis, et permet de faire la connection a la Base de donnees Redis selon
    l'environnement (dev ou test).
    Returns:
        Redis instance
    """
    global _redis_client


    is_testing = os.getenv('FLASK_TESTING', 'false').lower() == 'true'
    redis_db = int(os.getenv('REDIS_TEST_DB', 1)) if is_testing else int(os.getenv('REDIS_DB_USERS', 0))

    # Recreation du client redis si la BD change
    if _redis_client is not None:
        current_db = _redis_client.connection_pool.connection_kwargs.get('db')
        if current_db != redis_db:
            # DB a changé, recréer le client
            try:
                _redis_client.close()
            except Exception as e:
                print(f'Erreur lors de la fermeture de la connexion a redis: {e}')
                pass
            _redis_client = None

    # Creation du client redis si inexistant
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=redis_db,
                decode_responses=False
            )
            # Test de la connexion
            if _redis_client.ping() :
               print("Connexion établie avec success")
            else :
                raise redis.ConnectionError
        except Exception as e:
            print(f"Erreur de connexion à Redis: {e}")
            _redis_client = None
    return _redis_client



def reset_redis_client():
    """
        Fonction permettant de réinitialiser la connexion a Redis
    """

    global _redis_client

    if _redis_client is not None:
        try:
            _redis_client.close()
        except:
            pass
    _redis_client = None