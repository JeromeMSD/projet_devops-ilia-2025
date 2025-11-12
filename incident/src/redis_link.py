import redis
import json

# Connexion à Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
try:
    r.ping()
    print("✅ Connexion à Redis réussie !")
except redis.exceptions.ConnectionError as e:
    print(f"❌ Erreur de connexion : {e}")

def saveJSONFile(obj):
    """
    Sauvegarde un objet JSON dans Redis en utilisant son identifiant comme clé.
    
    Exemple :
        obj = {"id": 123, "title": "Incident", "status": "open"}
        saveJSONFile(obj)
        => Stocke dans Redis : key="INC:123", value="{...json...}"
    """
    try:
        # Vérification que 'id' existe dans l'objet
        if "id" not in obj:
            raise ValueError("L'objet JSON doit contenir un champ 'id' unique.")
        
        # Création de la clé
        key = f"INC:{obj['id']}"
        
        # Conversion de l'objet en texte JSON
        json_data = json.dumps(obj)
        
        # Enregistrement dans Redis
        r.set(key, json_data)
        
        print(f"✅ Objet enregistré dans Redis avec la clé {key}")
        return key
    
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return None
    
import time

# Création d'un objet JSON exemple
test_incident = {
    "id": int(time.time()),  # ID unique basé sur le timestamp
    "title": "Latence élevée API",
    "sev": "medium",
    "services": ["api-gateway", "auth-service"],  # Liste de services concernés
    "summary": "Temps de réponse > 2000ms sur le endpoint /login",
    "status": "open",           # Statut initial
    "started_at": int(time.time()),  # Timestamp UNIX de création
    "commander": None           # Aucun assigné pour l'instant
}

saveJSONFile(test_incident)