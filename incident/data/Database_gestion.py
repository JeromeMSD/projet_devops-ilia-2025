import redis
import time

# D'abord utiliser : pip install redis
# Puis dans un autre terminal : .\redis-server.exe
# Ensuite lancez le script python voulu afin d'utiliser correctement la base redis
# Enfin ouvrez un nouveau terminal et taper : .\redis-cli.exe 
# Puis taper les commandes qu'il faut (～￣▽￣)～ 👍 
# (Genre "KEY*" pour récuperer toutes les clés , ou "HGETALL INC:" suivit de la clé pour voir tout ce qu'elle contient)

try:
    r = redis.Redis(decode_responses=True)
    r.ping()
    print("Connexion à Redis réussie !")

    # On utilise un timestamp Unix pour la clé
    incident_timestamp = int(time.time())
    incident_key = f"INC:{incident_timestamp}" # Ex: "INC:1731390480"

    incident_data = {
        "source": "api-gateway",
        "duree": "2025.11.12.09.30.00", 
        "titre": "Latence élevée API",
        "description": "Latence > 2000ms sur le endpoint /login"
    }

    print(f"\nCréation de l'incident : {incident_key}")
    r.hset(incident_key, mapping=incident_data)
    
    # Lire toutes les données d'un coup
    data = r.hgetall(incident_key)
    print(f"\nDonnées complètes du Hash : \n{data}")

    # Lire un seul champ
    titre = r.hget(incident_key, "titre")
    print(f"\nTitre seul : {titre}")
    
    # On ajoute un nouveau champ "statut"
    r.hset(incident_key, "statut", "RESOLU")
    
    # On vérifie
    statut = r.hget(incident_key, "statut")
    print(f"Nouveau statut : {statut}")
    
    #Nettoyage 
    # r.delete(incident_key)
    # print(f"\nIncident {incident_key} supprimé.")


except redis.exceptions.ConnectionError as e:
    print(f"❌ Erreur de connexion à Redis : {e}")