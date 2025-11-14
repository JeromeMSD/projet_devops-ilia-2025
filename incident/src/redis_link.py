import redis
import json

# Connexion à Redis
try:
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    r.ping()
    print("Connexion à Redis réussie !")
except redis.exceptions.ConnectionError:
    print("Erreur : impossible de se connecter à Redis.")
    r = None


def saveJSONFile(obj):
    if r is None:
        print("Redis non connecté.")
        return None
    try:
        if "id" not in obj:
            raise ValueError("L'objet JSON doit contenir un champ 'id' unique.")
        key = obj["id"]
        json_data = json.dumps(obj)
        r.set(key, json_data)
        return obj
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        return None


def loadJSONFile(id):
    if r is None:
        print("Redis non connecté.")
        return None
    try:
        json_data = r.get(id)
        if json_data is None:
            return None
        return json.loads(json_data)
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
        return None
