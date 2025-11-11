import redis
import os

from dotenv import load_dotenv

load_dotenv()

USER_KEY = os.getenv('USER_KEY', 'user:')
EMAIL_KEY = os.getenv('EMAIL_KEY', 'email:')

# Redis connection configuration
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))


IS_TESTING = os.getenv('FLASK_TESTING').lower() == 'true'
if IS_TESTING:
    REDIS_DB = int(os.getenv('REDIS_TEST_DB'))
else:
    REDIS_DB = int(os.getenv('REDIS_DB_USERS'))


_redis_client = None

def get_redis_client():
    """
        Retourne une instance singleton du client Redis.
        Cette fonction crée une connexion Redis unique qui sera réutilisée
        dans toute l'application, évitant ainsi de créer plusieurs connexions.
        Returns:
            redis.Redis: Instance du client Redis ou None si la connexion échoue
    """
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB, 
                decode_responses=False
            )
            # Test de la connexion
            _redis_client.ping()
            print(f"✓ Connexion Redis établie: {REDIS_HOST}:{REDIS_PORT} (DB: {REDIS_DB} - MODE TEST: {IS_TESTING})")
        except Exception as e:
            print(f"✗ Erreur de connexion à Redis: {e}")
            _redis_client = None

    return _redis_client